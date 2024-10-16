'''
Author: galeliu
Date: 2024-10-15 19:31:20
LastEditTime: 2024-10-16 12:14:23
LastEditors: galeliu
Description: .
'''
import asyncio
import websockets
import json


async def hello():
    # uri = "ws://localhost:8765"
    uri = "ws://localhost:5001"
    async with websockets.connect(uri) as websocket:
        message = {'type': 'request_chain'}
        await websocket.send(json.dumps(message))

        response = await websocket.recv()
        print(response)


async def node_connect():
    # uri = "ws://localhost:8765"
    uri = "ws://localhost:5001"
    async with websockets.connect(uri) as websocket:
        message = {'type': 'request_chain'}
        await websocket.send(json.dumps(message))

        response = await websocket.recv()
        print(response)
asyncio.set_event_loop(asyncio.new_event_loop())
# asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_until_complete(node_connect())
