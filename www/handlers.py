__author__='llx'

import re,time,json,logging,hashlib,base64,asyncio
from coroweb import get,web
from WEB import User,Comment,Blog,next_id

loop=asyncio.get_event_loop()

@get('/')
async def index(request):
    # users=await User.findall()
    users='askdjfkasjk'
    logging.info('lalalla:%s'%users)

    return {
        '__template__': 'test.html',
        'users':users
    }
