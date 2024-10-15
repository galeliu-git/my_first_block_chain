'''
Author: galeliu
Date: 2024-10-15 12:01:17
LastEditTime: 2024-10-15 18:24:11
LastEditors: galeliu
Description: .
'''
import asyncio
import websockets
import json
import requests
from Blockchain import Blockchain, Block


class Node:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.peers = set()

    async def send_message(self, websocket, message):
        await websocket.send(json.dumps(message))

    async def handle_message(self, websocket, path):
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'new_block':
                self.handle_new_block(data['block_data'])
            elif data['type'] == 'new_transaction':
                self.handle_new_transaction(data['transaction_data'])
            elif data['type'] == 'request_chain':
                await self.send_chain(websocket)
            elif data['type'] == 'send_chain':
                self.handle_chain(data['chain'])

    def handle_new_block(self, block_data):
        block = Block(**block_data)
        # 验证当前区块是否有效
        if self.blockchain.is_valid_block(block):
            self.blockchain.chain.append(block)
            print('区块已添加到区块链中')
        else:
            print('收到的区块无效')
            print(block_data)

    def handle_new_transaction(self, transaction_data):
        transaction_index = self.blockchain.add_transcation(**transaction_data)
        print('交易已添加到交易池中，区块索引为：', transaction_index)

    async def send_chain(self, websocket):
        message = {
            'type': 'send_chain',
            'chain': [block.to_dict() for block in self.blockchain.chain]
        }
        await self.send_message(websocket, message)

    def handle_chain(self, chain_data):
        chain = [Block(**block_data) for block_data in chain_data]
        # 验证收到的链是否比当前链长，且有效
        if len(chain) > len(self.blockchain.chain) and self.blockchain.is_valid_chain(chain):
            self.blockchain.chain = chain
            print('区块链已更新')
        else:
            print('收到的区块链无效')

    async def connect_to_peer(self, peer):
        async with websockets.connect(peer) as websocket:
            self.peers.add(peer)
            message = {'type': 'request_chain'}
            await self.send_message(websocket, message)

    async def broadcast_new_block(self, block):
        message = {
            'type': 'new_block',
            'block_data': block.to_dict()
        }
        print('-----全网广播消息开始-----')
        for peer in self.peers:
            async with websockets.connect(peer) as websocket:
                await self.send_message(websocket, message)
        print('-----全网广播消息结束-----')
