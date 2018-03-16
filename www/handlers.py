__author__='llx'

import re,time,json,logging,hashlib,base64,asyncio
from coroweb import get,web
import inspect
from WEB import User,Comment,Blog,next_id

loop=asyncio.get_event_loop()

@get('/')
async def index(request):
    # users=await User.findall()
    users='askdjfkasjk'
    logging.info('lalalla:%s' %inspect.stack()[1][3])

    return {
        '__template__': 'test.html',
        'users':users
    }

@get('/base')
async def base(request):

    return {
        '__template__':'base.html',
    }

@get('/son')
async def son(request):

    return {
        '__template__':'son.html',
    }

@get('/b_son')
async def b_son(request):

    return{
        '__template__':'b_son.html',
    }