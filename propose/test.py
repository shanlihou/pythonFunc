# coding=utf-8
import asyncio

from aiohttp import web
from Lib.display import display


async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')


async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    display().drawPoint(15,  15, 0x889914, 9)
    display().display()
    return web.Response(body=text.encode('utf-8'))


async def loopOnce():
    display().loopOnce()
    return 1


async def displayLoop():
    while True:
        display().loopOnce()
        await asyncio.sleep(0.1)


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    display()
    return srv

loop = asyncio.get_event_loop()
tasks = [init(loop), displayLoop()]
loop.run_until_complete(asyncio.wait(tasks))
loop.run_forever()
