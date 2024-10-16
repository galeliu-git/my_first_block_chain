'''
Author: galeliu
Date: 2024-10-15 19:31:09
LastEditTime: 2024-10-15 19:51:37
LastEditors: galeliu
Description: .
'''
import asyncio
import websockets


async def echo(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")
        await websocket.send(f"Echo: {message}")

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
