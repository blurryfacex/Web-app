#
# if asked me what i learn today, i'll tell you i fucking leaned so much
# variable name you have to use `xxx` not 'xxx' fuck
#
from www import orm
from www.WEB import *

import asyncio
loop=asyncio.get_event_loop()
async def text():
    x=await orm.create_pool(loop=loop,host='127.0.0.1',port=3306,db='awesome',user='root',password='123456')
    U=await User.findall()
    print (U)
    # for i in range(2,10):
    #     u=User(name='Test',email='306965405@{0}.com'.format(str(i+10)),password='123456',image='about:blank',id='1234'+str(i+10))
    #     await u.save()


loop.run_until_complete(text())

