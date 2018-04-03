#
# if asked me what i learn today, i'll tell you i fucking leaned so much
# variable name you have to use `xxx` not 'xxx' fuck
#
import orm
#
# wtf , you import was wrong that fucked up ,man
#
from models import User

import asyncio

loop = asyncio.get_event_loop()
@asyncio.coroutine
def text(loop):
    yield from orm.create_pool(loop=loop,db='awesome',user='root',password='123456')
    x=yield from User.findAll()
    print (x)
    # u = User(name='Test', email='1234@qq.com', passwd='123456', image='about:blank', id='1234', admin='123')
    # yield from u.save()


# loop=asyncio.get_event_loop()
#
# async def text(loop):
#     x=await orm.create_pool(loop=loop,host='127.0.0.1',port=3306,db='awesome',user='root',password='123456')
#
#     for i in range(1,22):
#         u=User(name='Test',email='306965405@{0}.com'.format(str(i+10)),password='123456',image='about:blank',id='1234'+str(i+10))
#         u.save()
#
# loop.run_until_complete(text(loop))
loop.run_until_complete(text(loop))

