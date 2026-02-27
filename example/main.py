from itick.sdk import Client
import time

# 初始化客户端
token = "8850*****************ee4127087"
client = Client(token)

# 设置 WebSocket 消息处理器
def on_message(message):
    print(f"Received WebSocket message: {message}")

# 设置 WebSocket 错误处理器
def on_error(error):
    print(f"WebSocket error: {error}")

client.set_message_handler(on_message)
client.set_error_handler(on_error)

# 测试外汇实时成交接口
tick = client.get_forex_tick("GB", "EURUSD")
print("Forex Tick:", tick)

# 测试外汇实时报价接口
quote = client.get_forex_quote("GB", "EURUSD")
print("Forex Quote:", quote)

# 测试外汇实时盘口接口
depth = client.get_forex_depth("GB", "EURUSD")
print("Forex Depth:", depth)

# 测试外汇历史K线接口
kline = client.get_forex_kline("GB", "EURUSD", 2, 10)
print("Forex Kline:", kline)

# 测试 WebSocket 连接
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
