# coding=utf-8
import asyncio

from aiohttp import web
from aiohttp import web_runner
from RPC import RPC
import threading


async def cmd(request):
    data = await request.json()
    RPC().parseCmd(data)
    return web.json_response({'result': 'success'})


async def init(loop):
    app = web.Application(loop=loop)
    app = web_runner.AppRunner(app=app).app()
    app.router.add_post('/cmd/', cmd, expect_handler=web.Request.json)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv


def serverStart(*args):
    print('args:', args)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as e:
        print(e)
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()

    tasks = [init(loop)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.run_forever()


def serverThread():
    t = threading.Thread(target=serverStart, args=())
    t.start()


if __name__ == '__main__':
    print(111)
    serverThread()
