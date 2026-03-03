# iTick Python SDK

Python 语言版本的 iTick API SDK，提供基础、股票、指数、期货、基金、外汇、加密货币数据的 REST API 查询和 WebSocket 实时数据订阅功能。

# 官网地址：[https://itick.org](https://itick.org)

## 功能特性

- 支持 REST API 查询基础、股票、指数、期货、基金、外汇、加密货币数据
- 支持 WebSocket 实时数据订阅
- 自动重连机制
- 心跳保持连接
- 回调式事件处理

## 安装

```bash
pip install itick-sdk
```

或从源码安装：

```bash
cd python
pip install -e .
```

## 快速开始

### 初始化客户端

```python
from itick.sdk import Client

token = "your_api_token"
client = Client(token)
```

### REST API 使用

#### 外汇数据查询

```python
# 获取外汇实时成交
tick = client.get_forex_tick("GB", "EURUSD")
print("Forex Tick:", tick)

# 获取外汇实时报价
quote = client.get_forex_quote("GB", "EURUSD")
print("Forex Quote:", quote)

# 获取外汇实时盘口
depth = client.get_forex_depth("GB", "EURUSD")
print("Forex Depth:", depth)

# 获取外汇历史K线
kline = client.get_forex_kline("GB", "EURUSD", 2, 10)
print("Forex Kline:", kline)
```

#### 股票数据查询

```python
# 获取股票实时成交
tick = client.get_stock_tick("US", "AAPL")
print("Stock Tick:", tick)

# 获取股票实时报价
quote = client.get_stock_quote("US", "AAPL")
print("Stock Quote:", quote)

# 获取股票实时盘口
depth = client.get_stock_depth("US", "AAPL")
print("Stock Depth:", depth)

# 获取股票历史K线
kline = client.get_stock_kline("US", "AAPL", 2, 10)
print("Stock Kline:", kline)
```

#### 加密货币数据查询

```python
# 获取加密货币实时成交
tick = client.get_crypto_tick("BA", "BTCUSDT")
print("Crypto Tick:", tick)

# 获取加密货币实时报价
quote = client.get_crypto_quote("BA", "BTCUSDT")
print("Crypto Quote:", quote)

# 获取加密货币实时盘口
depth = client.get_crypto_depth("BA", "BTCUSDT")
print("Crypto Depth:", depth)

# 获取加密货币历史K线
kline = client.get_crypto_kline("BA", "BTCUSDT", 2, 10)
print("Crypto Kline:", kline)
```

### WebSocket 使用

SDK 提供了增强的 WebSocket 功能，包括自动重连和心跳保持，用户无需手动管理连接状态。

#### 设置回调函数

```python
# 设置消息处理器
def on_message(message):
    print(f"Received WebSocket message: {message}")

# 设置错误处理器
def on_error(error):
    print(f"WebSocket error: {error}")

client.set_message_handler(on_message)
client.set_error_handler(on_error)
```

#### 连接和订阅

```python
# 连接外汇 WebSocket
client.connect_forex_websocket()

# 发送订阅消息
client.send_websocket_message('{"action": "subscribe", "codes": ["EURUSD"]}')

# 等待接收消息
import time
time.sleep(10)

# 检查连接状态
print(f"WebSocket connected: {client.is_websocket_connected()}")

# 关闭 WebSocket
client.close_websocket()
```

#### 其他 WebSocket 连接

```python
# 连接股票 WebSocket
client.connect_stock_websocket()

# 连接加密货币 WebSocket
client.connect_crypto_websocket()
```

## API 接口列表

### 基础 (Basics)

| 方法 | 说明 |
|------|------|
| get_symbol_list | 获取符号列表 |
| get_symbol_holidays | 获取节假日信息 |

### 股票 (Stock)

| 方法 | 说明 |
|------|------|
| get_stock_info | 获取股票信息 |
| get_stock_ipo | 获取股票IPO信息 |
| get_stock_split | 获取股票分拆信息 |
| get_stock_tick | 获取股票实时成交 |
| get_stock_quote | 获取股票实时报价 |
| get_stock_depth | 获取股票实时盘口 |
| get_stock_kline | 获取股票历史K线 |
| get_stock_ticks | 获取股票批量实时成交 |
| get_stock_quotes | 获取股票批量实时报价 |
| get_stock_depths | 获取股票批量实时盘口 |
| get_stock_klines | 获取股票批量历史K线 |
| connect_stock_websocket | 连接股票 WebSocket |

### 指数 (Indices)

| 方法 | 说明 |
|------|------|
| get_indices_tick | 获取指数实时成交 |
| get_indices_quote | 获取指数实时报价 |
| get_indices_depth | 获取指数实时盘口 |
| get_indices_kline | 获取指数历史K线 |
| get_indices_ticks | 获取指数批量实时成交 |
| get_indices_quotes | 获取指数批量实时报价 |
| get_indices_depths | 获取指数批量实时盘口 |
| get_indices_klines | 获取指数批量历史K线 |
| connect_indices_websocket | 连接指数 WebSocket |

### 期货 (Futures)

| 方法 | 说明 |
|------|------|
| get_future_tick | 获取期货实时成交 |
| get_future_quote | 获取期货实时报价 |
| get_future_depth | 获取期货实时盘口 |
| get_future_kline | 获取期货历史K线 |
| get_future_ticks | 获取期货批量实时成交 |
| get_future_quotes | 获取期货批量实时报价 |
| get_future_depths | 获取期货批量实时盘口 |
| get_future_klines | 获取期货批量历史K线 |
| connect_future_websocket | 连接期货 WebSocket |

### 基金 (Funds)

| 方法 | 说明 |
|------|------|
| get_fund_tick | 获取基金实时成交 |
| get_fund_quote | 获取基金实时报价 |
| get_fund_depth | 获取基金实时盘口 |
| get_fund_kline | 获取基金历史K线 |
| get_fund_ticks | 获取基金批量实时成交 |
| get_fund_quotes | 获取基金批量实时报价 |
| get_fund_depths | 获取基金批量实时盘口 |
| get_fund_klines | 获取基金批量历史K线 |
| connect_fund_websocket | 连接基金 WebSocket |

### 外汇 (Forex)

| 方法 | 说明 |
|------|------|
| get_forex_tick | 获取外汇实时成交 |
| get_forex_quote | 获取外汇实时报价 |
| get_forex_depth | 获取外汇实时盘口 |
| get_forex_kline | 获取外汇历史K线 |
| get_forex_ticks | 获取外汇批量实时成交 |
| get_forex_quotes | 获取外汇批量实时报价 |
| get_forex_depths | 获取外汇批量实时盘口 |
| get_forex_klines | 获取外汇批量历史K线 |
| connect_forex_websocket | 连接外汇 WebSocket |

### 加密货币 (Crypto)

| 方法 | 说明 |
|------|------|
| get_crypto_tick | 获取加密货币实时成交 |
| get_crypto_quote | 获取加密货币实时报价 |
| get_crypto_depth | 获取加密货币实时盘口 |
| get_crypto_kline | 获取加密货币历史K线 |
| get_crypto_ticks | 获取加密货币批量实时成交 |
| get_crypto_quotes | 获取加密货币批量实时报价 |
| get_crypto_depths | 获取加密货币批量实时盘口 |
| get_crypto_klines | 获取加密货币批量历史K线 |
| connect_crypto_websocket | 连接加密货币 WebSocket |

## WebSocket 功能说明

### 自动重连

SDK 内置自动重连机制，当网络异常或连接断开时，会自动尝试重新连接：
- 重连间隔：5 秒
- 最大重连次数：10 次
- 重连成功后自动恢复订阅

### 心跳保持

SDK 自动维护 WebSocket 连接的心跳：
- 心跳间隔：30 秒
- 自动发送 ping 消息保持连接活跃

### 连接状态检查

```python
# 检查 WebSocket 是否连接
connected = client.is_websocket_connected()
```

## 完整示例

```python
from itick.sdk import Client
import time

# 初始化客户端
token = "your_api_token"
client = Client(token)

# 设置 WebSocket 消息处理器
def on_message(message):
    print(f"Received WebSocket message: {message}")

# 设置 WebSocket 错误处理器
def on_error(error):
    print(f"WebSocket error: {error}")

client.set_message_handler(on_message)
client.set_error_handler(on_error)

# 测试 REST API
tick = client.get_forex_tick("GB", "EURUSD")
print("Forex Tick:", tick)

# 测试 WebSocket
try:
    client.connect_forex_websocket()
    
    # 发送订阅消息
    client.send_websocket_message('{"action": "subscribe", "codes": ["EURUSD"]}')
    
    # 等待接收消息
    print("Waiting for WebSocket messages...")
    time.sleep(10)
    
    # 检查连接状态
    print(f"WebSocket connected: {client.is_websocket_connected()}")
    
finally:
    # 关闭 WebSocket
    client.close_websocket()
```

## 文档

详细 API 文档请参考：[https://docs.itick.org](https://docs.itick.org)

## 许可证

MIT License
