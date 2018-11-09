# coding=utf-8
import asyncio

from aiohttp import web
from aiohttp import web_runner
from RPC import RPC
from coco import start as cocoStart
from music import Music


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


def start():
    loop = asyncio.get_event_loop()
    tasks = [init(loop)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.run_forever()


if __name__ == '__main__':
    start()
