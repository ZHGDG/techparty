# -*- coding: utf-8 -*-
'''base: ms4py / bottle-wiki / source — Bitbucket
	https://bitbucket.org/ms4py/bottle-wiki/src/1586473a6ce1/auth.py
'''
from bottle import request, HTTPError
from functools import partial
from hashlib import sha256

from config import CFG

import sae.kvdb
KV = sae.kvdb.KVClient()


def sha256_uhex(data):
    ''' Generates unicode hex value of given data with SHA-256. '''
    return str(unicode(sha256(data).hexdigest()))
def check_login(username, password, fullpath):
    '''根据用户名,以及口令:
        - 明确是否登录
        - 明确是否有当前级别的权限!
    '''
    pw_hash = sha256_uhex(password)
    suname = sha256_uhex(username)
    usrid = "%s%s"% (CFG.PREUID, suname)
    crtusr = KV.get(usrid)
    #print fullpath.split("/")[1]
    #print type(CFG.LEVEL4USR[fullpath.split("/")[1]])
    #print type(crtusr['level'])
    if crtusr:
        crtPathLevel = CFG.LEVEL4USR[fullpath.split("/")[1]]
        if str(crtPathLevel) == str(crtusr['level']):
            print "'%s' had crt. path right ;-)"% username
            return True
        else:
            print "'%s' disallow crt. path ;-("% username
            return False
    else:
        print "'%s' NOT exist!"% username
        return False
    '''
    #print fullpath.split("/")[1]
    print CFG.LEVEL4USR[fullpath.split("/")[1]]
    usr = 1#KV.get("usr:%s"% str(sha256_uhex(username.decode('utf-8'))))
    if usr is None:
        return False
    #return usr.password == pw_hash
    return 1
    '''

def auth_required(check_func=check_login, realm='bottle-authentication'):
    """
    Decorator for basic authentication. 
    
    "check_func" has to be a callable object with two 
    arguments ("username" and "password") and has to return 
    a bool value if login was sucessful or not.
    """
    def decorator(view):
        def wrapper(*args, **kwargs):
            try:
                user, password = request.auth
            except (TypeError, AttributeError):
                # catch AttributeError because of bug in bottle
                auth = False
            else:
                auth = check_login(user, password, request.fullpath)
                #print "\t path: ", request.keys()
                #print request.fullpath
            if auth:
                return view(*args, **kwargs)
            return HTTPError(401, 'Access denied!', 
                header={'WWW-Authenticate': 'Basic realm="%s"' % realm})
        return wrapper
    return decorator


