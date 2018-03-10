#coding:utf-8
import logging;logging.basicConfig(level=logging.INFO)
import os,orm,json,time,asyncio

from datetime import datetime
from aiohttp import web
from jinja2 import Environment,FileSystemLoader
from coroweb import add_routes,add_static

#主体
async def index(request):
    return web.Response(body=b'<h1>Index</h1>',headers={'content-type':'text/html'})

async def init(loop):
    app=web.Application(loop=loop)
    app.router.add_route('GET','/',index)
    srv= await loop.create_server(app.make_handler(),'127.0.0.1',9000)
    logging.info('server started at http://127.0.0.1:9000')
    return srv

loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()


