'''
Author: galeliu
Date: 2024-10-15 19:23:34
LastEditTime: 2024-10-16 11:57:11
LastEditors: galeliu
Description: .
'''
import asyncio
import websockets
import json
str1 = '{"message":"\u8282\u70b9\u8fde\u63a5\u6210\u529f"}'
# 解码字符串
print(json.loads(str1))
