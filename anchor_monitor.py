
import time
from datetime import datetime
import requests
import json
from time import sleep
import math
import csv

"""
获取系统时间，如果为整点，获取 Anchor TVL，LUNA 价格推送 discord
"""
# 存储上一次数据变量，计算环比
LAST_TVL = 0.0
LAST_PRICE = 0.0

# 定义数据获取地址
deposit_url = 'https://api.anchorprotocol.com/api/v1/deposit'
collaterals_url = 'https://api.anchorprotocol.com/api/v1/collaterals'
apy_url = 'https://api.anchorprotocol.com/api/v1/market/ust'
price_url = 'https://api2.binance.com/api/v3/ticker/price?symbol=LUNAUSDT'

# 存上一次文件路径
csv_path = '/root/crypto-monitor/last_data.csv'

# 定义Webhook地址
webhook_url_1 = 'https://discord.com/api/webhooks/925220656797327401/KqaH0FDuRn51L2ro_I3Yh_T9dP4pr3mVGzNb9K4UNnVe0VXljzOCUZ7TODclkJ81kOo9' # personal
webhook_url_2 = 'https://discord.com/api/webhooks/924326162660991046/OjKmVKZwLbsjXzzGk_UI-E2igbmm-0OGXzZGeTfOAoN3H6kCQfQpaNh7fnCdE3WLaVG2' #sister


def get_data():

    headers = {
    }

    # 获取质押量
    req = requests.get(url=deposit_url, headers=headers)
    if req.status_code == 200:
        data = json.loads(req.text)
        total_deposits = float(data['total_ust_deposits'])/1000000
    else:
        print("请求码为{}, 获取 deposit 数据失败".format(req.status_code))
    
    # 获取抵押量
    req = requests.get(url=collaterals_url, headers=headers)
    
    if req.status_code == 200:
        data = json.loads(req.text)
        total_collaterals = float(data['total_value'])/1000000
    else:
        print("请求码为{}, 获取 collaterals 数据失败".format(req.status_code))

    # 获取质押APY
    req = requests.get(url=apy_url, headers=headers)
    
    if req.status_code == 200:
        data = json.loads(req.text)
        apy = float(data['deposit_apy'])
    else:
        print("请求码为{}, 获取质押收益数据失败".format(req.status_code))

    # 获取价格
    req = requests.get(url=price_url, headers=headers)
    
    if req.status_code == 200:
        data = json.loads(req.text)
        price = float(data['price'])
    else:
        print("请求码为{}, 获取价格数据失败".format(req.status_code))

    return total_deposits+total_collaterals,apy,price

# 获取上一次数据
with open(csv_path) as f:
    for line in f:
        row = line.split(',')
        LAST_PRICE = float(row[0])
        LAST_TVL = float(row[1])

# crontab 每个小时执行
data_time =  datetime.now()
tvl,apy,price = get_data()
tvl_diff = (tvl - LAST_TVL)/LAST_TVL
price_diff = (price - LAST_PRICE)/LAST_PRICE

data_time_display = data_time.strftime("%Y-%m-%d %H:%M:%S")
tvl_display = '{:,}'.format(math.floor(tvl))
apy_display = '{:.4%}'.format(apy)
tvl_diff_display = '{:.4%}'.format(tvl_diff)
price_diff_display = '{:.4%}'.format(price_diff)


# 更新上一次数据
row = [price,tvl]

# 以写模式打开文件
with open(csv_path, 'w', encoding='UTF8', newline='') as f:
    # 创建CSV写入器
    writer = csv.writer(f)

    # 向CSV文件写内容
    writer.writerow(row)


message = f"【Anchor 监控】\n{data_time_display}\nAPY: {apy_display}\ntvl: {tvl_display}  tvl环比: {tvl_diff_display}\nLuna 价格: {price}  Luna 价格环比: {price_diff_display}"
payload = {
    "username": "Monitor Cat",
    "content": message
}

# 打印
print(message)

# 推送discord
requests.post(webhook_url_1, json=payload)
requests.post(webhook_url_2, json=payload)



