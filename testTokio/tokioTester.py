#coding:utf-8

import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://localhost:9527') as websocket:

        await websocket.send('hello world')

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())