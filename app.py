'''
Author: galeliu
Date: 2024-10-14 17:41:00
LastEditTime: 2024-10-15 18:05:52
LastEditors: galeliu
Description: .
'''
from flask import Flask, request, jsonify
import Blockchain
from node import Node
import asyncio
import websockets
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
app = Flask(__name__)
blockchain = Blockchain.Blockchain()
node = Node(blockchain)


# 挖矿
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.get_last_block()
    # print(last_block)
    last_proof = last_block.proof
    # print(last_proof)
    # 计算工作量证明
    proof = blockchain.proof_of_work(last_proof)
    # print(proof)

    # 创建一个新的区块
    previous_hash = last_block.compute_hash()
    block = blockchain.create_block(proof, previous_hash)

    # 挖矿成功后，广播新快给所有节点
    asyncio.run(node.broadcast_new_block(block))
    response = {
        'message': '新的区块已被挖出',
        'index': block.index,
        'transactions': block.transactions,
        'proof': block.proof,
        'previous_hash': block.previous_hash
    }
    return jsonify(response), 200


# 添加新交易到区块链
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return '缺少参数', 400
    index = blockchain.add_transcation(
        values['sender'], values['recipient'], values['amount'])
    response = '交易将被添加到区块{}'.format(index)
    return jsonify(response), 201


# 查看完整区块链
@app.route('/full_chain', methods=['GET'])
def full_chain():
    response = {
        'chain': [block.to_dict() for block in blockchain.chain],
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


# 节点连接
@app.route('/nodes/connect', methods=['POST'])
def connect_node():
    values = request.get_json()
    peer = values.get('peer')
    if not peer:
        return '无效节点地址', 400
    print('请求连接节点地址：', peer)
    asyncio.run(node.connect_to_peer(peer))
    response = {
        'message': '节点连接成功',
    }
    return jsonify(response), 200


# 启动websocket服务
def start_p2p_server(host, port):
    '''用于节点间p2p通信，允许区块链节点互相连接'''
    loop = asyncio.new_event_loop()  # 创建新的事件循环
    asyncio.set_event_loop(loop)     # 将其设置为当前线程的事件循环
    loop.run_until_complete(websockets.serve(node.handle_message, host, port))
    print('P2P服务已启动，监听端口{}'.format(port))


if __name__ == '__main__':
    # thread = Thread(target=start_p2p_server, args=('0.0.0.0', 5001))
    # thread.start()
    # 启动websocket服务
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(start_p2p_server, '0.0.0.0', 5001)
    # 启动Flask服务
    app.run(host='0.0.0.0', port=5000)
