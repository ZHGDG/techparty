# -*- coding: utf-8 -*-
#import os
import sys
import time
import traceback
import zipfile
from copy import deepcopy
#from tempfile import TemporaryFile
#from StringIO import StringIO
#from shutil import copyfileobj
import json

import sae
import sae.storage
import sae.kvdb

from bottle import Bottle
from bottle import __version__ as bottleVer
from bottle import debug, run
from bottle import redirect, abort
from bottle import request, response, local
from bottle import static_file
from bottle import template
#from bottle import jinja2_view as view
#from bottle import jinja2_template as template
from bottle import jinja2_template as template
from bottle import TEMPLATE_PATH

import crx_id
#   120821 appended for SAE upgrade cancel Basic Author...
from auth import auth_required

from utility import INCR4KV as __incr
from utility import TSTAMP, GENID
from utility import POP4KV, POP4LIST, INS2LIST, IDX4LIST
from utility import ST4CRX, KV4CRX, KV4GRP
from utility import INIobjSYS, PUTHIS, PUT2SS, PUT_PIC4CRX



from config import CFG

#debug(True)
APP = Bottle()

KV = sae.kvdb.KVClient()
SG = sae.storage.Client()

@APP.route('/')
@auth_required()
def alertnoid():
    return template('upalertnoid.html')

@APP.route('/<gid>')
@auth_required()
def grpsee(gid):
    ''' realy ACTION:
        - get obj. by g:id
    ,'crxs':[]      # 已发布的
    ,'trys':[]      # 待发布的
    ,'outs':[]      # 被下架的
    '''
    crgrp = KV.get(gid)
    crxs = IDX4LIST(crgrp['crxs'], KV)
    trys = IDX4LIST(crgrp['trys'], KV)
    outs = IDX4LIST(crgrp['outs'], KV)
    baks = IDX4LIST(crgrp['baks'], KV)
    print "\t crxs ", crxs
    print "\t trys ", trys
    print "\t outs ", outs
    print "\t baks ", baks
    
    return template('upgrp.html'
        , grp = crgrp
        , crxs = crxs
        , trys = trys
        , outs = outs
        , baks = baks
        , gid = gid
        )

    #print crgrp['name']
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




@APP.route('/<gid>/ed')
@auth_required()
def grped(gid):
    ''' realy ACTION:
        - get obj. by g:id
    '''
    crgrp = KV.get(gid)
    return template('upgrped.html'
        , grp = crgrp
        , gid = gid
        )




@APP.route('/<gid>/info', method='POST')
def grpinfo(gid):
    ''' realy ACTION:
        - get values by POST, and set all into. by g:id
    '''
    name = request.forms.get('name')
    desc = request.forms.get('desc', '...') #request.files.get('data')
    crgrp = KV.get(gid)
    crgrp['name'] = name.decode('utf-8')
    crgrp['desc'] = desc.decode('utf-8')
    KV.set(gid, crgrp)
    redirect("/up/%s"% gid)
    
    '''
    crxs = IDX4LIST(crgrp['crxs'], KV)
    trys = IDX4LIST(crgrp['trys'], KV)
    outs = IDX4LIST(crgrp['outs'], KV)
    return template('upgrp.html'
        , grp = crgrp
        , crxs = crxs
        , trys = trys
        , outs = outs
        , gid = gid
        )
    '''



@APP.route('/<gid>/crx/add', method='POST')
@auth_required()
def addcrx(gid):
    '''初始/升级 .crx   realy ACTION:
        - chk manifest.json info:
            - if  uuid exist AND ver is up ->  
                + copy as x:id -> historic KVobj
                + up ver/desc/name
            - else ->
                + creat new crx KVobj
                + append uuid into SYS:trys
        - deepcopy(CFG.objCRX) set var with .crx
            - append uuid into CFG.K4D['uuid']
            - append uuid into CFG.K4D['try']
        - jump into /crx/x:id/info
    '''
    #print "\t>>> addcrx()"
    crxfile = request.files.get('crxfile', None) #request.files.get('data')
    if crxfile is not None:
        uuid = crx_id.GetCRXAppID4upload(crxfile.file)
        #   read manifest.json from crx file
        zz = zipfile.ZipFile(crxfile.file, "r")
        manifest = zz.open("manifest.json").read()
        #   fixed error JSON format from:"夜间模式.crx"
        json = eval(manifest.replace("\r\n",""))
        if KV.get(uuid):
            crtcrx = KV.get(uuid)
            if json['version'] == crtcrx['version']:
                # not any upgrade?!
                redirect("/up/%s/crx/%s/duplicate"% (gid, uuid) )
            else:
                # update try...
                #print "\n TRY update by uploading..."
                crx4update = deepcopy(crtcrx)
                xid = crx4update['id']
                crx4update['name'] = json['name'].decode('utf-8')
                crx4update['desc'] = json['description'].decode('utf-8')
                crx4update['version'] = json['version']
                #hid = PUTHIS(crtcrx, "U")
                #crx4update['hisid'] = crx4update['hisid'].append(hid)
                raw = crxfile.file.read() # This is dangerous for big files
                sid, uri = PUT2SS(raw, uuid, 'sae')
                crx4update['sid'] = sid
                crxfile.file.close()
                KV.set(uuid, crx4update)
                #print KV.get(uuid)
        else:
            # new .crx ;-)
            raw = crxfile.file.read() # This is dangerous for big files
            sid, uri = PUT2SS(raw, uuid, 'sae')
            crxfile.file.close()
            #   for create NEW crx
            crx = deepcopy(CFG.objCRX)
            xid = GENID('crx')
            crx['id'] = xid
            crx['uuid'] = uuid
            crx['sid'] = sid
            crx['grpid'] = gid  #<~~~ 关键行为!
            #hid = PUTHIS(crx, "C")
            #crx['hisid'] = crx['hisid'].append(hid)
            crx['name'] = json['name'].decode('utf-8')
            crx['desc'] = json['description'].decode('utf-8')
            crx['version'] = json['version']
            #print crx
            KV.add(uuid, crx)


            #   default try->pub ;-)
            KV4CRX(uuid, "try")

        #print "\tdata.file.closed? ", data.file.closed
        #LIST所有的domain
        #print ss.list_domain()
        #print "\tcrx4lb inc files:", len(ss.list(CFG.D2X))
        #print ss.url(CFG.D2X, sskey)

    uri = "/up/%s/crx/%s"% (gid, uuid)
    #print uri
    response.set_header('location', uri)
    response.status = 303
    #   redirect NOT WORK! abt.
    #redirect("/crx/%s/info"% tid, code=303)
    #https://github.com/defnull/bottle/issues/236
    #https://groups.google.com/forum/#!topic/bottlepy/RQV3B7ACiNk/discussion
    return None


@APP.route('/<gid>/crx/<uuid>/duplicate')
def crxduplicated(gid, uuid):
    ''' realy ACTION:
        - get obj. by uuid
        - alert DUPLICATE ERROR 
    '''
    crcrx = KV.get(uuid)
    #print crcrx
    return template('upcrxduplicated.html'
        , crx = crcrx
        , gid = gid
        , uuid = uuid
        )


@APP.route('/<gid>/crx/<uuid>')
@auth_required()
def seecrx(gid, uuid):
    crcrx = KV.get(uuid)
    #print "\tseecrx()", gid, uuid
    #print crcrx['name']
    incrx, intry, inout, inbak, inarch = ST4CRX(uuid)
    #print "\t incrx, intry, inout, inbak, inarch\n\t ",incrx, intry, inout, inbak, inarch
    #tags = crcrx['tagid']
    #print "\tcrcrx['tagid']", crcrx['tagid']
    tobjs = IDX4LIST(crcrx['tagid'], KV)
    #gobj = KV.get(gid)
    return template('upcrx.html'
        , crx = crcrx
        , incrx = incrx
        , intry = intry
        , inout = inout
        , inbak = inbak
        , inarch = inarch
        , gid = gid
        , uuid = uuid
        , tags = tobjs
        )


@APP.route('/<gid>/crx/<uuid>/ed')
@auth_required()
def crxed(gid, uuid):
    ''' realy ACTION:
        - get obj. by uuid
    '''
    crcrx = KV.get(uuid)
    k4tag, crtags = INIobjSYS('tag')
    tags = IDX4LIST(crtags, KV)
    #print tags, grps
    return template('upcrxed.html'
        , crx = crcrx
        , tags = tags
        , gid = gid
        , uuid = uuid
        )



@APP.route('/<gid>/crx/<uuid>/info', method='POST')
def crxinfo(gid, uuid):
    ''' realy ACTION:
        - set obj. vars base uuid
         if upload pic:
            + put into Storage
            + create new objPIC KV
            + append sid into SYS:pics
            + append sid into crx.pic
        + binding TAG
    '''
    picfile = request.files.get('picture', None) #request.files.get('data')
    if picfile is not None:
        filename = picfile.filename
        raw = picfile.file.read() # This is dangerous for big files
        sid, uri, crcrx = PUT_PIC4CRX(raw, filename, uuid)
    else:
        crcrx = KV.get(uuid)
    name = request.forms.get('name')
    desc = request.forms.get('desc', '...')
    tags = request.forms.getlist('tags')
    #    up CRX
    crcrx['name'] = name.decode('utf-8')
    crcrx['desc'] = desc.decode('utf-8')
    crcrx['tagid'] = tags
    KV.set(uuid, crcrx)
    #    up TAGS
    if tags:
        for t in tags:
            tag = KV.get(t)
            tag['crxs'] = INS2LIST(uuid, tag['crxs'])
            KV.set(t, tag)
    tobjs = IDX4LIST(tags, KV)
    #   return default grpcrx
    redirect("/up/%s/crx/%s"% (gid, uuid) )
    
    #print tobjs
    return template('upcrx.html'
        , crx = crcrx 
        , tags = tobjs 
        , gid = gid
        , uuid = uuid
        )



@APP.route('/<gid>/crx/<uuid>/pub')
@auth_required()
def crxpub(gid, uuid):
    ''' realy ACTION:
        - set uuid into:
            + SYS:trys[]
            + objGRP.objGRP[] <~~~
        - jump back
    for k in c.keys():
        print "\t%s:\t%s"% (k, c[k])
    '''
    #print "\t gid, uuid:", gid, uuid
    KV4CRX(uuid, "ini")  
    c = KV.get(uuid)
    grpcrxs, grptrys, grpouts, grpbaks = KV4GRP(uuid)
    #print "\t grpcrxs, grptrys, grpouts, grpbaks"
    #print "\t", grpcrxs, grptrys, grpouts, grpbaks
    #return None
    redirect("/up/%s"% gid) 



@APP.route('/<gid>/crx/<uuid>/pic/<sid>/ed')
@auth_required()
def crxpiced(gid, uuid, sid):
    '''edit. crx's pic:
        + get info. byr sid
    '''
    #print uuid, sid
    crtpic = KV.get(sid)
    #print crtpic
    #return None
    return template('upcrxpic.html'
        , gid = gid
        , uuid = uuid 
        , sid = sid
        , pic = crtpic
        )




@APP.route('/<gid>/crx/<uuid>/pic/<sid>/see', method='POST')
def crxpicsee(gid, uuid, sid):
    '''confirmed crx pic's editor:
        + get info. byr sid
    '''
    note = request.forms.get('note', '...')
    #print uuid, sid
    crtpic = KV.get(sid)
    crtpic['note'] = note.decode('utf-8')
    KV.set(sid, crtpic)
    #return None
    return template('upseepic.html'
        , gid = gid
        , uuid = uuid 
        , sid = sid 
        , pic = crtpic
        )
@APP.route('/<gid>/crx/<uuid>/pic/<sid>/del')
def crxpicdel(gid, uuid, sid):
    '''del. crx's pic:
        + del. SS obj
        + pop sid from SYS:pics
        + pop sid from crx.pic
        + set pic['isdel'] = 1
    '''
    #print uuid, sid
    try:
        ss = sae.storage.Client()
        ss.delete(CFG.D2P, sid)
        #print "\tKV.get(k4pic)", KV.get(k4pic)
    except:
        print ">>>/crx/<xid>/pic/<sid>/del \n\t", traceback.print_exc()
    #   + pop sid from SYS:pic
    k4pic, crpics = INIobjSYS('pic')
    POP4KV(sid, k4pic, crpics)
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
    uri = "/up/%s/crx/%s"% (gid,uuid)
    #print uri
    redirect(uri)    
    #response.set_header('location', uri)
    #response.status = 303
    #redirect(uri)




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
    

