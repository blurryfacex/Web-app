# coroutine

# def consumer():
#     r=''
#     while True:
#         t=yield r
#         if not t:
#             return
#         print ('[Consumer] %s' %t)
#         r='200 OK'
#
# def produce(c):
#     c.send(None)
#     count=0
#     while count<5:
#         count+=1
#         print ('[produce] %s' %count)
#         r=c.send(count)
#         print ('[produce] return %s' %r)
#     c.close()
#
# c=consumer()
# produce(c)

# asyncio
import asyncio

# @asyncio.coroutine
# def hello():
#     print ('Hello World')
#     r=yield from asyncio.sleep(1)
#
#     print ('Hello again')
#
# loop=asyncio.get_event_loop()
# taks=[hello(),hello()]
# loop.run_until_complete(asyncio.wait(taks))
# loop.close()


# @asyncio.coroutine
# def wget(host):
#     print ('wget %s'%host)
#     connect=asyncio.open_connection(host,80)
#     reader,write=yield from connect
#     header='GET / HTTP/1.0\r\nHost: %s\r\n\r\n' %host
#     write.write(header.encode('utf-8'))
#     yield from write.drain()
#     while True:
#         line=yield from reader.readline()
#         print (line)
#         if line==b'\r\n':
#             break
#         print ('%s header > %s' %(host,line.decode("utf-8").rstrip()))
#     write.close()
#
#
# loop=asyncio.get_event_loop()
# tasks=[wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()


# async & await grammar

# async def hello():
#     print ('hello ')
#     y=await asyncio.sleep(1)
#     print ('hhh')
#
#
# loop=asyncio.get_event_loop()
# task=[hello(),hello()]
# loop.run_until_complete(asyncio.wait(task))
# loop.close()

#aiohttp

# from aiohttp import web
#
# async def index(request):
#     await asyncio.sleep(0.5)
#     return web.Response(body=b'<h1>Index</h1>')
#
# async def hello(request):
#     await asyncio.sleep(0.5)
#     text='<h1>hello,%s</h1>' %request.match_info['name']
#     return web.Response(body=text.encode('utf-8'))
#
# async def init(loop):
#     app=web.Application(loop=loop)
#     app.router.add_route('GET','/',index)
#     app.router.add_route('GET','/hello',hello)
#     recv=await loop.create_server(app.make_handler(),'127.0.0.1',8000)
#     print ('server started at http://127.0.0.1:8000...')
#     return recv
#
# loop=asyncio.get_event_loop()
# loop.run_until_complete(init(loop))
# loop.run_forever()
