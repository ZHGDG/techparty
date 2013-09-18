# -*- coding: utf-8 -*-
#import os
import time
import traceback
import zipfile
#import json as JSON
from copy import deepcopy

import pprint
pp = pprint.PrettyPrinter(indent=4)
#from tempfile import TemporaryFile
#from StringIO import StringIO
#from shutil import copyfileobj
import sae
import sae.storage
import sae.kvdb

from bottle import Bottle
from bottle import debug, run
from bottle import redirect, abort
from bottle import request, response, local
from bottle import static_file
#from bottle import template
#from bottle import jinja2_view as view
from bottle import jinja2_template as template
from bottle import TEMPLATE_PATH

import crx_id
#   120821 appended for SAE upgrade cancel Basic Author...
from auth import auth_required

from utility import INCR4KV as __incr
from utility import TSTAMP, GENID
from utility import POP4KV, POP4LIST, INS2LIST, INS2DICT4LIST, IDX4LIST
from utility import ST4CRX, KV4CRX, KV4GRP
from utility import INIobjSYS, PUTHIS, PUT2SS, PUT_PIC4CRX

from config import CFG

debug(True)
APP = Bottle()

KV = sae.kvdb.KVClient()
SG = sae.storage.Client()

@APP.route('/usrs')
@auth_required()
def usrs():
    sysk, crusrs = INIobjSYS('usr')
    if 0 == len(crusrs):
        objusrs = None
    else:
        objusrs = []
        for uid in crusrs:
            #print uid
            #print KV.get(uid)
            objusrs.append(KV.get(uid))
    return template('authors.html', usrs=objusrs)

#@view('404.html')
@APP.error(404)
def error404(error):
    return template('404.html')

@APP.route('/favicon.ico')
def favicon():
    abort(204)
    
@APP.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')
    
@APP.route('/')
@auth_required()
def mana():
    return template('mana.html')
    





@APP.route('/gen')
@auth_required()
def genall():
    '''gen all can gen pages:
        - dict of pages idx:
            + tag include pages
            + all pages uri
        tags={
            tid:{TAG's norm. dict data
                + "pub":{
                    xid:{CRX's norm. dict data}
                    ,,,}
                ,,,}
            ,,,}
    '''
    k4tags, crttags = INIobjSYS('tag')
    k4pubs, crtpubs = INIobjSYS('crx')
    #print crttags
    tags = []
    for tag in crttags:
        crxtag = KV.get(tag)
        crxtag['pub'] = []
        for xid in crxtag['crxs']:
            if xid in crtpubs:
                crxtag['pub'].append(KV.get(xid))
            else:
                #print KV.get(xid)['ispub']
                pass
        tags.append(crxtag)
    '''
    for k in tags.keys():
        print tags[k]['pub'].keys()
    '''
    return template('gen.html'
        , tags = tags
        )
    





@APP.route('/gen/crx/<uuid>.html')
def gencrx(uuid):
    #print "get it!"
    crtcrx = KV.get(uuid)
    crtgrp = KV.get(crtcrx['grpid'])
    page = template('gencrx.html'
        , crx = crtcrx
        , grp = crtgrp
        )
    #print page
    sid, uri = PUT2SS(page.encode('utf-8'), uuid, 'html')
    #print sid, uri
    redirect(uri)

    return template('gencrx.html'
        , crx = crtcrx
        , grp = crtgrp
        )
    





@APP.route('/gen/<tid>.html')
def gentag(tid):
    '''gen all can gen pages:
        - dict of pages idx:
            + tag include pages
            + all pages uri
        tags={
            tid:{TAG's norm. dict data
                + "pub":{
                    xid:{CRX's norm. dict data}
                    ,,,}
                ,,,}
            ,,,}
    '''
    k4tags, crttags = INIobjSYS('tag')
    tags = []
    for t in crttags:
        tag = KV.get(t)
        tags.append({'id':tag['id'],'name':tag['name']})
    #return Nonr
    
    k4pubs, crtpubs = INIobjSYS('crx')
    crttag = KV.get(tid)
    crttag['pub'] = []
    for xid in crttag['crxs']:
        if xid in crtpubs:
            crttag['pub'].append(KV.get(xid))
    print "\t crttag['pub']:", len(crttag['pub'])
    # every 3 app.s as 1 <UL>
    ulcrxs = []
    ul = 0
    licrxs = []
    for crx in crttag['pub']:
        crtgrp = KV.get(crx['grpid'])
        page = template('gencrx.html'
            , crx = crx
            , grp = crtgrp
            )
        #print page
        sid, uri = PUT2SS(page.encode('utf-8'), crx['id'], 'html')
        #print sid, uri

        crx['pageuri'] = uri
        ul += 1
        if 0 == ul%3:
            licrxs.append(crx)
            ulcrxs.append(licrxs)
            licrxs = []
        else:
            licrxs.append(crx)
    if 0 != len(licrxs):
        ulcrxs.append(licrxs)
        
    #print "\t ulcrxs:", len(ulcrxs)
    #print "\t ulcrxs[0]", len(ulcrxs[0])
    page = template('gentag.html'
        , crtid = tid
        , tags = tags
        , crttag = ulcrxs
        )
    sid, uri = PUT2SS(page.encode('utf-8'), tid, 'html')
    #print sid, uri
    redirect(uri)

    return template('gentag.html'
        , crtid = tid
        , tags = tags
        , crttag = ulcrxs
        )
    





@APP.route('/crxs')
@auth_required()
def crxs():
    ''' realy ACTION:
        - listing all crx with ctrl links
    '''
    k4crx, crcrxs = INIobjSYS('crx')
    k4try, crtrys = INIobjSYS('try')
    k4out, crouts = INIobjSYS('out')
    k4bak, crbaks = INIobjSYS('bak')
    k4arch, crxarch = INIobjSYS('arch')
    #print KV.get(k4crx)
    obj4crx = IDX4LIST(crcrxs, KV)
    obj4try = IDX4LIST(crtrys, KV)
    obj4out = IDX4LIST(crouts, KV)
    obj4bak = IDX4LIST(crbaks, KV)
    obj4arch = IDX4LIST(crxarch, KV)
    if obj4crx: print "\t obj4crx=", len(obj4crx)
    if obj4try: print "\t obj4try=", len(obj4try)
    if obj4out: print "\t obj4out=", len(obj4out)
    if obj4bak: print "\t obj4bak=", len(obj4bak)
    if obj4arch: print "\t obj4arch=", len(obj4arch)
    #print obj4crx
    return template('crxs.html'
        , obj4crx = obj4crx
        , obj4try = obj4try
        , obj4out = obj4out
        , obj4bak = obj4bak
        , obj4arch = obj4arch
        )


@APP.route('/crx/ini', method='POST')
def inicrx():
    '''初始/升级 .crx   realy ACTION:
        - chk manifest.json info:
            - if  uuid exist AND ver is up ->  
                + copy as x:id -> historic KVobj
                + up ver/desc/name
            - else ->
                + creat new crx KVobj
        - deepcopy(CFG.objCRX) set var with .crx
            - append uuid into CFG.K4D['uuid']
            - append uuid into CFG.K4D['try']
        - jump into /crx/x:id/info
    '''
    crxfile = request.files.get('crxfile', None) #request.files.get('data')
    if crxfile is not None:
        #filename = crxfile.filename
        uuid = crx_id.GetCRXAppID4upload(crxfile.file)
        #print '\tAppID:\t%s' % uuid
        #   read manifest.json from crx file
        zz = zipfile.ZipFile(crxfile.file, "r")
        manifest = zz.open("manifest.json").read()
        #   fixed error JSON format from:"夜间模式.crx"
        manifest.replace("\r\n","")
        #print manifest
        json = {}
        for l in manifest.split(','):
            if '"name":' in l:
                #print l
                json['name'] = l.split(':')[1].split("\"")[1]
            elif '"version":' in l:
                print l
                json['version'] = l.split(':')[1].split("\"")[1]
                #print l.split(':')[1][2:-1]
            elif '"description":' in l:
                #print l
                json['description'] = l.split(':')[1].split("\"")[1]
            else:
                pass

        #print "\t", json['name'], json['description'], json['version']
        #return None
        #json = eval(manifest)
        #json = JSON.loads(manifest.decode('utf-8'))
        if KV.get(uuid):
            crtcrx = KV.get(uuid)
            if json['version'] == crtcrx['version']:
                # not any upgrade?!
                redirect("/mana/crx/%s/duplicate"% uuid)
            else:
                # update try...
                #print "\n TRY update by uploading..."
                crx4update = deepcopy(crtcrx)
                #   120822 fixed by:UnicodeDecodeError - PythonInfo Wiki
                #	http://wiki.python.org/moin/UnicodeDecodeError
                crx4update['name'] = json['name'].decode('utf-8', "replace")
                crx4update['desc'] = json['description'].decode('utf-8', "replace")
                crx4update['version'] = json['version']
                #hid = PUTHIS(crtcrx, "U")
                #crx4update['hisid'] = crx4update['hisid'].append(hid)
                raw = crxfile.file.read() # This is dangerous for big files
                sid, uri = PUT2SS(raw, uuid, 'sae')
                crx4update['sid'] = sid
                crxfile.file.close()
                KV.set(uuid, crx4update)
                #print KV.get(uuid)
                xid = crx4update['id']
        else:
            #   new .crx ;-)
            raw = crxfile.file.read() # This is dangerous for big files
            sid, uri = PUT2SS(raw, uuid, 'sae')
            crxfile.file.close()
            #print "\tdata.file.closed? ", data.file.closed
            crx = deepcopy(CFG.objCRX)
            xid = GENID('crx')
            crx['id'] = xid
            crx['uuid'] = uuid
            crx['sid'] = sid
            #hid = PUTHIS(crx, "C")
            #crx['hisid'] = crx['hisid'].append(hid)
            crx['name'] = json['name'].decode('utf-8', "replace")
            crx['desc'] = json['description'].decode('utf-8', "replace")
            crx['version'] = json['version']
            #print crx
            KV.add(uuid, crx)
            crcrxs, crtrys, crouts, crbaks, crarch, ctcapi = KV4CRX(uuid, "ini")

            '''
            sskey = "%s.crx"% GENID('sae', uuid) #"%s-%s.crx"% (uuid, TSTAMP())
            #   初始化一个Storage客户端。
            ss = sae.storage.Client()
            ob = sae.storage.Object(raw)
            ss.put(CFG.D2X, sskey, ob)
            '''
        #print "\tdata.file.closed? ", data.file.closed
        #LIST所有的domain
        #print ss.list_domain()
        #print "\tcrx4lb inc files:", len(ss.list(CFG.D2X))
        #print ss.url(CFG.D2X, sskey)

        
    uri = "/mana/crx/%s"% uuid
    #print uri
    response.set_header('location', uri)
    response.status = 303
    #   redirect NOT WORK! abt.
    #redirect("/crx/%s/info"% tid, code=303)
    #https://github.com/defnull/bottle/issues/236
    #https://groups.google.com/forum/#!topic/bottlepy/RQV3B7ACiNk/discussion
    return None


@APP.route('/crx/<uuid>')
@auth_required()
def crxsee(uuid):
    '''realy ACTION:
        - get obj. by uuid
    '''
    #print uuid
    crcrx = KV.get(uuid)
    #print crcrx
    #print crcrx['name']
    incrx, intry, inout, inbak, inarch = ST4CRX(uuid)
    tags = crcrx['tagid']
    #print "\t crcrx['grpid']:", crcrx['grpid']
    tobjs = IDX4LIST(tags, KV)
    grp = crcrx['grpid']
    if grp:
        gobj = KV.get(grp)
    else:
        gobj = None
    #print "\t tags", tobjs
    return template('crx.html'
        , crx = crcrx 
        , incrx = incrx 
        , intry = intry 
        , inout = inout 
        , inbak = inbak
        , inarch = inarch 
        , tags = tobjs 
        , grp = gobj 
        )







@APP.route('/crx/<uuid>/ed')
@auth_required()
def crxed(uuid):
    ''' realy ACTION:
        - get obj. by uuid
    '''
    crcrx = KV.get(uuid)
    pp.pprint(crcrx)
    print "\tcrcrx.grpid", crcrx['grpid']
    k4tag, crtags = INIobjSYS('tag')
    k4grp, crgrps = INIobjSYS('grp')
    #print "\tk4grp, crgrps", k4grp, crgrps
    tags = IDX4LIST(crtags, KV)
    grps = IDX4LIST(crgrps, KV)
    print "\tgrps::", grps
    return template('crxed.html'
        , crx = crcrx
        , tags = tags
        , grps = grps
        )


@APP.route('/crx/jsini')
def jsini():
    '''初始/升级 .js   realy ACTION:
        - 填写 UUID 
        - deepcopy(CFG.objCRX) set var with .crx
            - append uuid into CFG.K4D['uuid']
            - append uuid into CFG.K4D['try']
        - jump into /crx/x:id/info
    '''
    crcrx = {}
    k4tag, crtags = INIobjSYS('tag')
    k4grp, crgrps = INIobjSYS('grp')
    #print "\tk4grp, crgrps", k4grp, crgrps
    tags = IDX4LIST(crtags, KV)
    grps = IDX4LIST(crgrps, KV)
    print "\tgrps::", grps
    return template('ujsed.html'
        , crx = crcrx
        , tags = tags
        , grps = grps
        )
@APP.route('/crx/jsup', method='POST')
def jsup():
    '''初始/升级 .js   realy ACTION:
        - 填写 UUID 
        - deepcopy(CFG.objCRX) set var with .crx
            - append uuid into CFG.K4D['uuid']
            - append uuid into CFG.K4D['try']
        - jump into /crx/x:id/info
    '''
    ujsfile = request.files.get('ujsfile') #request.files.get('data')
    if ujsfile is not None:
        uuid = request.forms.get('uuid')
        name = request.forms.get('name')
        desc = request.forms.get('desc')
        detail = request.forms.get('detail')
        version = request.forms.get('version')
        isreco = request.forms.get('isreco', 'noreco')
        #print isreco
        dlrank = request.forms.get('dlrank')

        if KV.get(uuid):
            crtcrx = KV.get(uuid)
            if version == crtcrx['version']:
                # not any upgrade?!
                redirect("/mana/crx/%s/duplicate"% uuid)
            else:
                # update try...
                #print "\n TRY update by uploading..."
                crx4update = deepcopy(crtcrx)
                #   120822 fixed by:UnicodeDecodeError - PythonInfo Wiki
                #	http://wiki.python.org/moin/UnicodeDecodeError
                crx4update['name'] = name.decode('utf-8', "replace")   #'].decode('utf-8', "replace")
                crx4update['desc'] = desc.decode('utf-8', "replace")   #json['description'].decode('utf-8', "replace")
                crx4update['version'] = version
                #hid = PUTHIS(crtcrx, "U")
                #crx4update['hisid'] = crx4update['hisid'].append(hid)
                raw = ujsfile.file.read() # This is dangerous for big files
                sid, uri = PUT2SS(raw, uuid, 'sae')
                crx4update['sid'] = sid
                ujsfile.file.close()
                KV.set(uuid, crx4update)
                #print KV.get(uuid)
                xid = crx4update['id']

        else:
            #   new .js ;-)
            raw = ujsfile.file.read() # This is dangerous for big files
            #print raw
            sid, uri = PUT2SS(raw, uuid, 'sae')
            ujsfile.file.close()
            #print "\tdata.file.closed? ", data.file.closed
            crx = deepcopy(CFG.objCRX)
            xid = GENID('crx')
            crx['id'] = xid
            crx['uuid'] = uuid
            crx['sid'] = sid
            #hid = PUTHIS(crx, "C")
            #crx['hisid'] = crx['hisid'].append(hid)
            crx['name'] = name.decode('utf-8', "replace")          #.decode('utf-8', "replace")
            crx['desc'] = desc.decode('utf-8', "replace")   #.decode('utf-8', "replace")
            crx['version'] = version
            #print crx
            KV.add(uuid, crx)
            crcrxs, crtrys, crouts, crbaks, crarch, ctcapi = KV4CRX(uuid, "ini")
    
    uri = "/mana/crx/%s"% uuid
    #print uri
    response.set_header('location', uri)
    response.status = 303
    #   redirect NOT WORK! abt.
    #redirect("/crx/%s/info"% tid, code=303)
    #https://github.com/defnull/bottle/issues/236
    #https://groups.google.com/forum/#!topic/bottlepy/RQV3B7ACiNk/discussion
    return None


@APP.route('/crx/<uuid>/info', method='POST')
@auth_required()
def crxinfo(uuid):
    ''' realy ACTION:
        - set obj. vars base uuid
         if upload pic:
            + put into Storage
            + create new objPIC KV
            + append sid into SYS:pics
            + append sid into crx.pic
        + binding TAG/GRP
    '''
    picfile = request.files.get('picture', None) #request.files.get('data')
    if picfile is not None:
        filename = picfile.filename
        raw = picfile.file.read() # This is dangerous for big files
        sid, uri, crcrx = PUT_PIC4CRX(raw, filename, uuid)
    else:
        crcrx = KV.get(uuid)
    name = request.forms.get('name')
    desc = request.forms.get('desc')
    detail = request.forms.get('detail')
    version = request.forms.get('version')
    isreco = request.forms.get('isreco', 'noreco')
    #print isreco
    dlrank = request.forms.get('dlrank')
    gsdl = request.forms.get('gsdl')
    gsusr = request.forms.get('gsusr')
    gsrank = request.forms.get('gsrank')
    
    tags = request.forms.getlist('tags')
    grp = request.forms.get('grp')
    print "\tgrp,tags:\n\t", grp,tags
    #return None
    
    crcrx['name'] = name.decode('utf-8')
    crcrx['desc'] = desc.decode('utf-8')
    crcrx['detail'] = detail.decode('utf-8')
    crcrx['version'] = version
    if "isreco"==isreco:
        crcrx['isreco'] = 1
    else:
        crcrx['isreco'] = 0
    crcrx['dlrank'] = dlrank
    crcrx['gsdl'] = gsdl
    crcrx['gsusr'] = gsusr
    crcrx['gsrank'] = gsrank

    crcrx['tagid'] = tags
    crcrx['grpid'] = grp
    KV.set(uuid, crcrx)
    if tags:
        for t in tags:
            tag = KV.get(t)
            tag['crxs'] = INS2LIST(uuid, tag['crxs'])
            KV.set(t, tag)
        
    if grp:
        grpcrxs, grptrys, grpouts, grpbaks = KV4GRP(uuid)
        '''
        crtgrp = KV.get(grp)
        incrx, intry, inout, inarch = ST4CRX(uuid)
        #crtgrp['']
        if incrx:
            #crtgrp['crxs'] = grp
            crtgrp['crxs'] = INS2LIST(uuid, crtgrp['crxs'])
            POP4LIST(uuid, crtgrp['trys'])
            POP4LIST(uuid, crtgrp['outs'])
        elif intry:
            POP4LIST(uuid, crtgrp['crxs'])
            crtgrp['trys'] = INS2LIST(uuid, crtgrp['trys'])
            POP4LIST(uuid, crtgrp['outs'])
        elif inout:
            POP4LIST(uuid, crtgrp['crxs'])
            POP4LIST(uuid, crtgrp['trys'])
            crtgrp['outs'] = INS2LIST(uuid, crtgrp['outs'])
        elif incrx:
            POP4LIST(uuid, crtgrp['crxs'])
            POP4LIST(uuid, crtgrp['crxs'])
            POP4LIST(uuid, crtgrp['outs'])
        KV.set(grp, crtgrp)
        '''
    
    redirect("/mana/crx/%s"% uuid)
    #tobjs = IDX4LIST(tags, KV)
    #gobj = KV.get(grp)
    
    '''
    return template('crx.html'
        , crx = crcrx 
        , tags = tobjs 
        , grp = gobj 
        )
    '''






@APP.route('/crx/<uuid>/duplicate')
def crxduplicated(uuid):
    ''' realy ACTION:
        - get obj. by uuid
        - alert DUPLICATE ERROR 
    '''
    crcrx = KV.get(uuid)
    #print crcrx
    return template('crxduplicated.html', crx = crcrx)


@APP.route('/crx/<uuid>/pic/<sid>/del')
def delpic(uuid, sid):
    '''del. crx's pic:
        + del. SS obj
        + pop sid from SYS:pics
        + pop sid from crx.pic
        + set pic['isdel'] = 1
    '''
    print uuid, sid
    try:
        ss = sae.storage.Client()
        ss.delete(CFG.D2P, sid)
        #print "\tKV.get(k4pic)", KV.get(k4pic)
    except:
        print ">>>/crx/<xid>/pic/<sid>/del \n\t", traceback.print_exc()
        #sys.exit(1)
        #return None
    #return None
    #   + pop sid from SYS:pic
    k4pic, crpics = INIobjSYS('pic')
    POP4KV(sid, k4pic, crpics)
    #print KV.get(k4pic)
    #   + pop sid from crx.pic
    crx = KV.get(uuid)
    crpics = crx['pic']
    POP4LIST(sid, crpics)   #crpics.pop(crpics.index(sid))
    crx['pic'] = crpics
    KV.set(uuid, crx)
    #   + set pic['isdel'] = 1
    pic = KV.get(sid)
    pic['isdel'] = 1
    KV.set(sid, pic)

    #print "\tKV.set(uuid)['pic']:", KV.get(uuid)['pic']
    redirect("/mana/crx/%s"% uuid)

    





@APP.route('/crx/<uuid>/pic/<sid>/ed')
@auth_required()
def edpic(uuid, sid):
    '''edit. crx's pic:
        + get info. byr sid
    '''
    #print uuid, sid
    crtpic = KV.get(sid)
    #print crtpic
    ss = sae.storage.Client()
    ssuri = ss.url(CFG.D2P, sid)
    #return None
    return template('crxpic.html'
        , uuid = uuid 
        , sid = sid
        , pic = crtpic
        , ssuri =ssuri
        )

    





@APP.route('/crx/<uuid>/pic/<sid>/see', method='POST')
def seepic(uuid, sid):
    '''confirmed crx pic's editor:
        + get info. byr sid
    '''
    note = request.forms.get('note', '...')
    icon = request.forms.get('icon', 'noicon')
    #print icon
    crtcrx = KV.get(uuid)
    crtpic = KV.get(sid)
    crtpic['note'] = note.decode('utf-8')
    if "icon"==icon:
        crtpic['icon'] = 1
        crtcrx['icon'] = sid
    else:
        crtpic['icon'] = 0
        crtcrx['icon'] = None
    KV.set(sid, crtpic)
    
    #return None
    return template('seepic.html'
        , uuid = uuid 
        , sid = sid 
        , pic = crtpic
        )

    





@APP.route('/pubs')
@auth_required()
def crxpubs():
    ''' realy ACTION:
        - list obj. from CFG.K4D['try']
    '''
    #print INIobjSYS('pub')
    sysk, crtpubs = INIobjSYS('try')
    if 0 == len(crtpubs):
        objcrxs = None
    else:
        objcrxs = []
        for xid in crtpubs:
            #print xid
            #print KV.get(xid)
            objcrxs.append(KV.get(xid))
    #print sysk, crtpubs
    #print objcrxs
    return template('crxpubs.html'
        , crxs4try=objcrxs
        )


@APP.route('/crx/<uuid>/try/<act>')
@auth_required()
def crxtry(uuid, act):
    ''' realy ACTION:
        - get obj. by uuid
        - exp. as page for confirmed
        - jump into page by ACT
    '''
    #print act
    crcrx = KV.get(uuid)
    #print crcrx
    return template('crxtry.html', crx = crcrx, jump = act)


@APP.route('/crx/<uuid>/pub', method='POST')
def crxpub(uuid):
    ''' realy ACTION:
        - set ispub == 1
            - set all abt. KV append/remove uuid
            - see utility.KV4CRX
        - jump bak /mana/crxs
    '''
    #name = request.forms.get('name')
    #desc = request.forms.get('desc', '...')
    reply = request.forms.get('reply', '...') 
    try:
        #print uuid
        crcrx = KV.get(uuid)
        #print crcrx
        crcrx['ispub'] = 1
        #crcrx['name'] = name.decode('utf-8')
        #crcrx['desc'] = desc.decode('utf-8')
        crcrx['reply'] = reply.decode('utf-8')
        KV.set(uuid, crcrx)
        # SYS idx.s fixed
        KV4CRX(uuid, 'pub')
    except:
        # cancel reDel,
        print ">>>/mana/crx/:uuid/pub \n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    KV4GRP(uuid)
    redirect("/mana/pubs")
    #return "deleting %s"% tid


@APP.route('/crx/<uuid>/out', method='POST')
def crxout(uuid):
    ''' realy ACTION:
        - set ispub == 0
            - set all abt. KV append/remove uuid
            - see utility.KV4CRX
        - jump bak /mana/crxs
    '''
    try:
        #print uuid
        crcrx = KV.get(uuid)
        #print crcrx
        crcrx['ispub'] = 0
        KV.set(uuid, crcrx)
        # SYS idx.s fixed
        KV4CRX(uuid, 'out')
    except:
        # cancel reDel,
        print ">>>/mana/crx/:uuid/out \n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    KV4GRP(uuid)
    redirect("/mana/pubs")
    #return "deleting %s"% tid


@APP.route('/crx/<uuid>/bak', method='POST')
def crxbak(uuid):
    ''' realy ACTION:
        - set ispub == 0
            - set all abt. KV append/remove uuid
            - see utility.KV4CRX
        - jump bak /mana/crxs
    '''
    reply = request.forms.get('reply')
    try:
        crcrx = KV.get(uuid)
        crcrx['ispub'] = 0
        crcrx['reply'] = reply.decode('utf-8')
        KV.set(uuid, crcrx)
        # SYS idx.s fixed
        KV4CRX(uuid, 'bak')
    except:
        # cancel reDel,
        print ">>>/mana/crx/:uuid/bak \n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    KV4GRP(uuid)
    redirect("/mana/pubs")
    #return "deleting %s"% tid


@APP.route('/crx/<uuid>/arch', method='POST')
def crxarch(uuid):
    ''' realy ACTION:
        - set ispub = 0 isdel = 1
            - set all abt. KV append/remove uuid
            - see utility.KV4CRX
        - jump bak /mana/crxs
    '''
    try:
        #print uuid
        crcrx = KV.get(uuid)
        #print crcrx
        crcrx['ispub'] = 0
        crcrx['isdel'] = 1
        KV.set(uuid, crcrx)
        # SYS idx.s fixed
        KV4CRX(uuid, 'arch')
    except:
        # cancel reDel,
        print ">>>/mana/crx/:uuid/bak \n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    KV4GRP(uuid)
    redirect("/mana/pubs")
    #return "deleting %s"% tid


@APP.route('/crx/<uuid>/recover', method='POST')
def crxrecover(uuid):
    ''' realy ACTION:
        - set ispub = 0 isdel = 0
            - set all abt. KV append/remove uuid
            - see utility.KV4CRX
        - jump bak /mana/crxs
    '''
    try:
        #print uuid
        crcrx = KV.get(uuid)
        #print crcrx
        crcrx['ispub'] = 0
        crcrx['isdel'] = 0
        KV.set(uuid, crcrx)
        # SYS idx.s fixed
        KV4CRX(uuid, 'recover')
    except:
        # cancel reDel,
        print ">>>/mana/crx/:uuid/bak \n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    KV4GRP(uuid)
    redirect("/mana/pubs")
    #return "deleting %s"% tid




@APP.route('/tags')
@auth_required()
def tags():
    ''' realy ACTION:
        - listing all tag with ctrl links
    '''
    sysk, crtags = INIobjSYS('tag')
    #print sysk, crtags
    #print KV.get(sysk)
    #print len(crtags)
    if 0 == len(crtags):
        objtags = None
    else:
        objtags = []
        for tid in crtags:
            #print tid
            #print KV.get(tid)
            objtags.append(KV.get(tid))
    return template('tags.html', tags=objtags)


@APP.route('/tag/ini', method='POST')
def initag():
    ''' realy ACTION:
        - deepcopy(CFG.objTAG) updeta with from
        - appended t:id into CFG.K4D['tag']
        - jump into /tag/t:id/info
    '''
    name = request.forms.get('name')
    desc = request.forms.get('desc', '...') #request.files.get('data')
    #print name, desc
    #print GENID('tag')
    tag =  deepcopy(CFG.objTAG)
    #print "CFG.objTAG id: ", id(CFG.objTAG)
    #print "tag id: ", id(tag)
    tid = GENID('tag')
    tag['id'] = tid
    tag['name'] = name.decode('utf-8')
    tag['desc'] = desc.decode('utf-8')
    #print tag
    sysk, crtags = INIobjSYS('tag')
    #print sysk, crtags
    try:
        KV.add(tid, tag)
        #print ">>>  collection all TAGs"
        crtags.append(tid)  # return None !!!!
        KV.set(sysk, crtags)
        uri = "/mana/tag/%s"% tid
        #print uri
        #redirect("/tag/%s/info"% tid, code=303)
        response.set_header('location', uri)
        response.status = 303
        #redirect NOT WORK! abt.
        #https://github.com/defnull/bottle/issues/236
        #https://groups.google.com/forum/#!topic/bottlepy/RQV3B7ACiNk/discussion
    except:
        print ">>>/mana/tag/ini\n\t", traceback.print_exc()
        #sys.exit(1)
        return None
        
    #return None


@APP.route('/tag/<tid>')
def tagsee(tid):
    ''' realy ACTION:
        - get obj. by t:id
    '''
    #print tid
    #print INIobjSYS('tag')
    crtag = KV.get(tid)
    crxs = IDX4LIST(crtag['crxs'], KV)
    return template('tag.html'
        , tag=crtag
        , crxs=crxs
        )


    '''
    print "\t>>>", crtag['crxs']
    cli = []
    for i in crtag['crxs']:
        if "t:" == i[:2]:
            print i
        else:
            cli.append(i)
    print cli
    crtag['crxs'] = cli
    KV.set(tid, crtag)
    '''

@APP.route('/tag/<tid>/ed')
@auth_required()
def taged(tid):
    ''' realy ACTION:
        - get obj. by t:id
    '''
    #print tid
    #print INIobjSYS('tag')
    crtag = KV.get(tid)
    #print crtag
    return template('taged.html', tag=crtag)


@APP.route('/tag/<tid>/del')
def tagdel(tid):
    ''' realy ACTION:
        - set isdel == 1
        - remove t:id from CFG.K4D['tag']
    '''
    sysk, crtags = INIobjSYS('tag')
    try:
        #print tid
        crtag = KV.get(tid)
        #print crtag
        crtag['isdel'] = 1
        KV.set(tid, crtag)
        crtags.pop(crtags.index(tid))
        KV.set(sysk, crtags)    # VERY NEED
    except:
        # cancel reDel,
        print ">>>/mana/tag/../del \n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    redirect("/mana/tags")
    #return "deleting %s"% tid


@APP.route('/tag/<tid>/info', method='POST')
def taginfo(tid):
    ''' realy ACTION:
        - set obj. vars base t:id
    '''
    name = request.forms.get('name')
    desc = request.forms.get('desc', '...') #request.files.get('data')
    #print name, desc
    #print INIobjSYS('tag')
    crtag = KV.get(tid)
    crtag['name'] = name.decode('utf-8')
    crtag['desc'] = desc.decode('utf-8')
    KV.set(tid, crtag)
    #print crtag
    redirect("/mana/tag/%s"% tid)
    #return template('tag.html', tag=crtag)



@APP.route('/grps')
@auth_required()
def grps():
    ''' realy ACTION:
        - listing all grp with ctrl links
    '''
    sysk, crgrps = INIobjSYS('grp')
    #print sysk, crgrps
    #print KV.get(sysk)
    #print len(crgrps)
    if 0 == len(crgrps):
        objgrps = None
    else:
        objgrps = []
        for gid in crgrps:
            #print gid
            #print KV.get(gid)
            objgrps.append(KV.get(gid))
    return template('grps.html', grps=objgrps)


@APP.route('/grp/ini', method='POST')
def inigrp():
    ''' realy ACTION:
        - deepcopy(CFG.objGRP) updeta with from
        - appended g:id into CFG.K4D['grp']
        - jump into /grp/g:id/info
    '''
    name = request.forms.get('name')
    desc = request.forms.get('desc', '...') 
    grp =  deepcopy(CFG.objGRP)
    #print "CFG.objTAG id: ", id(CFG.objTAG)
    #print "tag id: ", id(tag)
    gid = GENID('grp')
    grp['id'] = gid
    grp['name'] = name.decode('utf-8')
    grp['desc'] = desc.decode('utf-8')
    #print grp
    sysk, crgrps = INIobjSYS('grp')
    #print sysk, crgrps
    try:
        KV.add(gid, grp)
        crgrps.append(gid)  # return None !!!!
        KV.set(sysk, crgrps)
        uri = "/mana/grp/%s"% gid
        #print uri
        #redirect("/tag/%s/info"% tid, code=303)
        response.set_header('location', uri)
        response.status = 303
        #redirect NOT WORK! abt.
        #https://github.com/defnull/bottle/issues/236
        #https://groups.google.com/forum/#!topic/bottlepy/RQV3B7ACiNk/discussion
    except:
        print ">>>/mana/tag/ini\n\t", traceback.print_exc()
        #sys.exit(1)
        return None
        
    #return None


@APP.route('/grp/<gid>')
def grpsee(gid):
    ''' realy ACTION:
        - get obj. by g:id
    ,'crxs':[]      # 已发布的
    ,'trys':[]      # 待发布的
    ,'outs':[]      # 被下架的
    '''
    crgrp = KV.get(gid)
    #print "\t crgrp['baks']:", crgrp['baks']
    crxs = IDX4LIST(crgrp['crxs'], KV)
    trys = IDX4LIST(crgrp['trys'], KV)
    outs = IDX4LIST(crgrp['outs'], KV)
    baks = IDX4LIST(crgrp['baks'], KV)
    #print "\tcrxs,trys,outs\n\t", crxs, trys, outs
    return template('grp.html'
        , grp = crgrp
        , crxs = crxs
        , trys = trys
        , outs = outs
        , baks = baks
        )


    '''
    print "\tcrgrp.crxs/trys/outs\n\t", crgrp['crxs'], crgrp['trys'], crgrp['outs']
    cli = []
    for i in crgrp['trys']:
        if "g:" == i[:2]:
            print i
        else:
            cli.append(i)
    print "\tcli:", cli
    crgrp['trys'] = cli
    KV.set(gid, crgrp)
    '''
@APP.route('/grp/<gid>/ed')
@auth_required()
def grped(gid):
    ''' realy ACTION:
        - get obj. by g:id
    '''
    #print gid
    #print INIobjSYS('grp')
    crgrp = KV.get(gid)
    #print crgrp
    return template('grped.html', grp = crgrp)


@APP.route('/grp/<gid>/info', method='POST')
@auth_required()
def grpinfo(gid):
    ''' realy ACTION:
        - set obj. vars base g:id
    '''
    name = request.forms.get('name')
    desc = request.forms.get('desc', '...') #request.files.get('data')
    lead = request.forms.get('lead')
    weibo = request.forms.get('weibo')
    mail = request.forms.get('mail')
    #print name, desc
    #print INIobjSYS('grp')
    crgrp = KV.get(gid)
    crgrp['name'] = name.decode('utf-8')
    crgrp['desc'] = desc.decode('utf-8')
    crgrp['lead'] = lead.decode('utf-8')
    crgrp['weibo'] = weibo.decode('utf-8')
    crgrp['mail'] = mail
       
    KV.set(gid, crgrp)
    #print crgrp
    redirect("/mana/grp/%s"% gid)
    #return template('grp.html', grp=crgrp)


@APP.route('/grp/<gid>/del')
def grpdel(gid):
    ''' realy ACTION:
        - set isdel == 1
        - remove g:id from CFG.K4D['grp']
    '''
    sysk, crgrps = INIobjSYS('grp')
    try:
        #print gid
        crgrp = KV.get(gid)
        #print crgrp
        crgrp['isdel'] = 1
        KV.set(gid, crgrp)
        crgrps.pop(crgrps.index(gid))
        KV.set(sysk, crgrps)    # VERY NEED
        #print KV.get(gid)
    except:
        # cancel reDel,
        print ">>>/mana/grp/../del \n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    redirect("/mana/grps")
    #return "deleting %s"% tid






