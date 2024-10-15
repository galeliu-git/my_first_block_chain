'''
Author: galeliu
Date: 2024-10-14 15:09:12
LastEditTime: 2024-10-15 15:03:36
LastEditors: galeliu
Description: .
'''
import hashlib
import hashlib
import json
from time import time


# 区块
class Block:
    def __init__(self, index, previous_hash, transactions, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time()

    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'transactions': self.transactions,
            'proof': self.proof,
            'timestamp': self.timestamp
        }

    # 计算区块的哈希值

    def compute_hash(self):
        block_string = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


# 区块链
class Blockchain:
    def __init__(self):
        self.chain = []
        # 当前交易列表
        self.current_transactions = []
        # 创建创世区块
        self.create_block(proof=100, previous_hash='1')

    # 创建区块
    def create_block(self, proof, previous_hash):
        block = Block(
            index=len(self.chain)+1,
            previous_hash=previous_hash,
            transactions=self.current_transactions,
            proof=proof
        )
        # 清空当前交易
        self.current_transactions = []
        self.chain.append(block)
        return block

    # 获取最后一个区块
    def get_last_block(self):
        return self.chain[-1]

    # 新增交易
    def add_transcation(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        # 返回将添加到的一个区块的索引
        return self.get_last_block().index+1

    # 计算工作量
    def proof_of_work(self, last_proof):
        proof = 0
        while self.is_valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    # 验证工作量有效
    def is_valid_proof(self, last_proof, proof):
        guess = '{}{}'.format(last_proof, proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    # 验证是否为有效区块
    def is_valid_block(self, block):
        if block.index == 0:
            return True
        previous_block = self.chain[block.index-1]
        if block.previous_hash != previous_block.compute_hash():
            print('区块无效，前一个区块的哈希值不匹配')
            return False
        if self.is_valid_proof(previous_block.proof, block.proof) is False:
            print('区块无效，工作量证明不正确')
            return False
        return True

    # 验证给定区块链是否有效
    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            block = chain[i]
            if self.is_valid_block(block) is False:
                return False
            # previous_block = chain[i-1]
            # if block.previous_hash != previous_block.compute_hash():
            #     return False
            # if self.is_valid_proof(previous_block.proof, block.proof) is False:
            #     return False
        return True
