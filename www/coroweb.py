#coding:utf-8
from typing import Any

__author__='llx'
import asyncio,os,inspect,logging,functools
from urllib import parse
from aiohttp import web
from www.apis import ApiError

'''
    wraps useage: 
    
from functools import wraps
def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print func.__name__ + " was called"
        return func(*args, **kwargs)
    return with_logging
 
@logged
def f(x):
   """does some math"""
   return x + x * x
 
print f.__name__  # prints 'f' if not use wraps the awser will be with_looging
print f.__doc__ 
#-----------------------------------------------------------------------------
    inspect useage:
def text(*sd,d,df,n=1,i=0,m=0,):
    pass

aa=inspect.signature(text).parameters
for i,ty in aa.items():
    print (ty.kind)
# VAR_POSITIONAL
# KEYWORD_ONLY
# KEYWORD_ONLY
# KEYWORD_ONLY
# KEYWORD_ONLY
# KEYWORD_ONLY

'''

def get(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        wrapper.__method__='GET'
        wrapper.__route__=path
        return wrapper
    return decorator

def post(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        wrapper.__method__='POST'
        wrapper.__route__=path
        return wrapper
    return decorator

def get_required_kw_args(fn):
    args=[]
    params=inspect.signature(fn).parameters
    for name,param in params.items():
        if param.kind==inspect.Parameter.KEYWORD_ONLY and param.default==inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

def get_named_kw_args(fn):
    args=[]
    params=inspect.signature(fn).parameters
    for name,param in params.items():
        if param.kind==inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)

def has_name_kw_arg(fn):
    params=inspect.signature(fn).parameters
    for name,param in params.items():
        if param==inspect.Parameter.KEYWORD_ONLY:
            return True

def has_var_kw_arg(fn):
    params=inspect.signature(fn).parameters
    for name,param in params.items():
        if param==inspect.Parameter.VAR_KEYWORD:
            return True

def has_request_arg(fn):
    sig=inspect.signature(fn)
    params=sig.parameters
    found=False
    for name,param in params.items():
        if name=='request':
            found=True
            continue
        if found and (param.kind!=inspect.Parameter.VAR_KEYWORD and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_POSITIONAL):
            raise ValueError('request parameter must be last named parameter in function:%s%s' %(fn.__name__,str(sig)))
    return found

class RequestHandler(object):

    def __init__(self,app,fn):
        self._app=app
        self._func=fn
        self._has_request_arg=has_request_arg(fn)
        self._has_var_kw_arg=has_var_kw_arg(fn)
        self._has_name_kw_arg=has_name_kw_arg(fn)
        self._get_name_kw_args=get_named_kw_args(fn)
        self._get_required_kw_args=get_required_kw_args(fn)

    async def __call__(self,request):
        kw=None
        if self._has_name_kw_arg or self._has_var_kw_arg or self._has_request_arg:
            if request.method=='POST':
                if not request.content_type:
                    return web.HTTPBadRequest('Missing Content-type.')
                cn=request.content_type.lower()
                if cn.startswith('application/json'):
                    params=await request.json()
                    if not isinstance(params,dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw=params
                elif cn.startswith('application/x-www-form-urlencoded') or cn.startswith('mutipart/form-data'):
                    params=await request.post()
                    kw=dict(**params)
                else:
                    return web.HTTPBadRequest('Unsupoorted Content-Type:%s' %request.content_type)

            if request.method=='GET':
                qs=request.query_string
                if qs:
                    kw=dict()
                    for k,v in parse.parse_qs(qs,True).items():
                        kw[k]=v[0]

        if kw is None:
            kw=dict(**request.match_info)
        else:
            if not self._has_var_kw_arg and self._get_name_kw_args:
                copy=dict()
                for v in self._get_name_kw_args:
                    if v in kw:
                        copy[v]=kw[v]
            for k,v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args:%s' %kw)
                kw[k]=v
        if self._has_request_arg:
            kw['request']=request
        if self._get_required_kw_args:
            for name in self._get_required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest('Missing Argment:%s' %name)
        logging.info('call wit args:%s'%str(kw))

        try:
            r=await self._func(**kw)
            return r
        except ApiError as e:
            return dict(error=e.error,data=e.data,message=e.data)

def add_static(app):
    path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'static')
    app.router.add_static('/static/',path)
    logging.info('add static %s==>%s' %('/static/',path))

def add_route(app,fn):
    method=getattr(fn,'__method__',None)
    path=getattr(fn,'__route__',None)
    if path is None or method is None:
        raise ValueError('@get and @port is not defined:%s' %str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn=asyncio.coroutine(fn)
    logging.info('add route %s %s ==> %s(%s)' %(method,path,fn.__name__,', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method,path,RequestHandler(app,fn))

def add_routes(app,module_name):
    n=module_name.rfind('.')
    if n==(-1):
        #__import__() 函数用于动态加载类和函数
        mod=__import__(module_name,globals(),locals())
    else:
        name=module_name[n+1:]
        mod=getattr(__import__(module_name[:n],globals(),locals(),[name]),name)
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn=getattr(mod,attr)
        if callable(fn):
            method=getattr(fn,'__method__',None)
            path=getattr(fn,'__route__',None)
            if method and path:
                add_route(app,fn)


