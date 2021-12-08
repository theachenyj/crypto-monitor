
import time
from datetime import datetime
import requests
import json
from time import sleep
import math

"""
获取系统时间，如果为整点，获取 Anchor TVL，LUNA 价格推送 discord
"""
# 存储上一次数据变量，计算环比
LAST_TVL = 0.0
LAST_PRICE = 0.0

# 定义数据获取地址
deposit_url = 'https://api.anchorprotocol.com/api/v1/deposit'
collaterals_url = 'https://api.anchorprotocol.com/api/v1/collaterals'
price_url = 'https://api2.binance.com/api/v3/ticker/price?symbol=LUNAUSDT'

# 定义Webhook地址
webhook_url = 'https://discord.com/api/webhooks/918127616056242227/MIltISrE00cy87DHL6qrHyHwTWFzoOMSUqrkWEJ8_A1RxSwyCD-9XuDwa-isoYIo9jNS'


def get_data():

    headers = {
    }

    # 获取质押量
    req = requests.get(url=deposit_url, headers=headers)
    if req.status_code == 200:
        data = json.loads(req.text)
        total_deposits = float(data['total_ust_deposits'])
    else:
        print("请求码为{}, 获取 deposit 数据失败".format(req.status_code))
    
    # 获取抵押量
    req = requests.get(url=collaterals_url, headers=headers)
    
    if req.status_code == 200:
        data = json.loads(req.text)
        total_collaterals = float(data['total_value'])
    else:
        print("请求码为{}, 获取 collaterals 数据失败".format(req.status_code))

    # 获取价格
    req = requests.get(url=price_url, headers=headers)
    
    if req.status_code == 200:
        data = json.loads(req.text)
        price = float(data['price'])
    else:
        print("请求码为{}, 获取价格数据失败".format(req.status_code))

    return total_deposits+total_collaterals,price

# 初始化
LAST_TVL,LAST_PRICE = get_data()

# 每个小时执行
while True:
    data_time =  datetime.now()
    tvl,price = get_data()
    tvl_diff = (tvl - LAST_TVL)/LAST_TVL
    price_diff = (price - LAST_PRICE)/LAST_PRICE

    data_time_display = data_time.strftime("%Y-%m-%d %H:%M:%S")
    tvl_display = '{:,}'.format(math.floor(tvl))
    tvl_diff_display = '{:.4%}'.format(tvl_diff)
    price_diff_display = '{:.4%}'.format(price_diff)


    # 更新上一次数据
    LAST_TVL = tvl
    LAST_PRICE = price

    message = f"【（测试）Anchor 监控】\n{data_time_display}\ntvl: {tvl_display}  tvl环比: {tvl_diff_display}\nLuna 价格: {price}  Luna 价格环比: {price_diff_display}"
    payload = {
        "username": "Monitor Cat",
        "content": message
    }

    # 打印
    print(message)

    # 推送discord
    requests.post(webhook_url, json=payload)

    sleep(3600)



