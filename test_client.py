#!/usr/bin/env python3

from itick.sdk.client import Client


def main():
    # 使用真实API密钥
    token = "8850*****************ee4127087"
    client = Client(token)

    # 测试基础模块
    print("=== 测试基础模块 ===")
    try:
        symbol_list = client.get_symbol_list()
        print("get_symbol_list 成功")
    except Exception as e:
        print(f"get_symbol_list 错误: {e}")

    try:
        symbol_holidays = client.get_symbol_holidays()
        print("get_symbol_holidays 成功")
    except Exception as e:
        print(f"get_symbol_holidays 错误: {e}")

    # 测试股票模块
    print("\n=== 测试股票模块 ===")
    try:
        stock_info = client.get_stock_info("us", "AAPL")
        print("get_stock_info 成功")
    except Exception as e:
        print(f"get_stock_info 错误: {e}")

    try:
        stock_tick = client.get_stock_tick("us", "AAPL")
        print("get_stock_tick 成功")
    except Exception as e:
        print(f"get_stock_tick 错误: {e}")

    # 测试指数模块
    print("\n=== 测试指数模块 ===")
    try:
        indices_tick = client.get_indices_tick("us", "SPX")
        print("get_indices_tick 成功")
    except Exception as e:
        print(f"get_indices_tick 错误: {e}")

    # 测试期货模块
    print("\n=== 测试期货模块 ===")
    try:
        future_tick = client.get_future_tick("us", "ES")
        print("get_future_tick 成功")
    except Exception as e:
        print(f"get_future_tick 错误: {e}")

    # 测试基金模块
    print("\n=== 测试基金模块 ===")
    try:
        fund_tick = client.get_fund_tick("us", "SPY")
        print("get_fund_tick 成功")
    except Exception as e:
        print(f"get_fund_tick 错误: {e}")

    # 测试外汇模块
    print("\n=== 测试外汇模块 ===")
    try:
        forex_tick = client.get_forex_tick("forex", "EURUSD")
        print("get_forex_tick 成功")
    except Exception as e:
        print(f"get_forex_tick 错误: {e}")

    # 测试加密货币模块
    print("\n=== 测试加密货币模块 ===")
    try:
        crypto_tick = client.get_crypto_tick("crypto", "BTCUSD")
        print("get_crypto_tick 成功")
    except Exception as e:
        print(f"get_crypto_tick 错误: {e}")

    # 测试WebSocket
    print("\n=== 测试WebSocket ===")
    try:
        client.connect_stock_websocket()
        print("connect_stock_websocket 成功")
        client.close_websocket()
    except Exception as e:
        print(f"connect_stock_websocket 错误: {e}")

    print("\n所有测试完成")


if __name__ == "__main__":
    main()
