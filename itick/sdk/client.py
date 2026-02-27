import requests
import websocket
import json
import threading
import time

class Client:
    BASE_URL = "https://api.itick.org"
    WSS_URL = "wss://api.itick.org"
    
    # WebSocket constants
    PING_INTERVAL = 30  # seconds
    RECONNECT_INTERVAL = 5  # seconds
    MAX_RECONNECT_ATTEMPTS = 10
    
    def __init__(self, token):
        self.token = token
        self.ws = None
        self.ws_path = None
        self.ws_connected = False
        self.reconnect_attempts = 0
        self.running = False
        self.message_handler = None
        self.error_handler = None
        self.ping_thread = None
        self.read_thread = None
        self.reconnect_thread = None
        self.lock = threading.Lock()
    
    def _get(self, path, params):
        url = self.BASE_URL + path
        headers = {
            "accept": "application/json",
            "token": self.token
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(f"API error: {data.get('msg')}")
        return data.get("data")
    
    # WebSocket methods with enhanced functionality
    
    def set_message_handler(self, handler):
        """Set callback for received WebSocket messages"""
        self.message_handler = handler
    
    def set_error_handler(self, handler):
        """Set callback for WebSocket errors"""
        self.error_handler = handler
    
    def connect_websocket(self, path):
        """Establish WebSocket connection with automatic reconnection"""
        self.ws_path = path
        self.running = True
        self._connect_websocket()
    
    def _connect_websocket(self):
        """Internal method to establish WebSocket connection"""
        with self.lock:
            if not self.running:
                return
            
            try:
                url = self.WSS_URL + self.ws_path
                headers = {
                    "token": self.token
                }
                self.ws = websocket.create_connection(url, header=headers)
                self.ws_connected = True
                self.reconnect_attempts = 0
                
                # Start ping thread
                self.ping_thread = threading.Thread(target=self._ping_loop)
                self.ping_thread.daemon = True
                self.ping_thread.start()
                
                # Start read thread
                self.read_thread = threading.Thread(target=self._read_loop)
                self.read_thread.daemon = True
                self.read_thread.start()
                
            except Exception as e:
                if self.error_handler:
                    self.error_handler(e)
                self.ws_connected = False
                self._schedule_reconnect()
    
    def _ping_loop(self):
        """Send periodic ping messages to keep connection alive"""
        while self.running:
            time.sleep(self.PING_INTERVAL)
            with self.lock:
                if self.ws and self.ws_connected:
                    try:
                        self.ws.ping()
                    except Exception as e:
                        if self.error_handler:
                            self.error_handler(e)
                        self.ws_connected = False
                        self._schedule_reconnect()
    
    def _read_loop(self):
        """Read messages from WebSocket"""
        while self.running:
            with self.lock:
                if not self.ws or not self.ws_connected:
                    time.sleep(0.1)
                    continue
            
            try:
                message = self.ws.recv()
                if self.message_handler:
                    self.message_handler(message)
            except Exception as e:
                if self.error_handler:
                    self.error_handler(e)
                with self.lock:
                    self.ws_connected = False
                self._schedule_reconnect()
    
    def _schedule_reconnect(self):
        """Schedule reconnection attempt"""
        if self.reconnect_attempts >= self.MAX_RECONNECT_ATTEMPTS:
            if self.error_handler:
                self.error_handler(Exception("Max reconnect attempts reached"))
            return
        
        self.reconnect_attempts += 1
        if not self.reconnect_thread or not self.reconnect_thread.is_alive():
            self.reconnect_thread = threading.Thread(target=self._reconnect_loop)
            self.reconnect_thread.daemon = True
            self.reconnect_thread.start()
    
    def _reconnect_loop(self):
        """Attempt to reconnect"""
        time.sleep(self.RECONNECT_INTERVAL)
        if self.running:
            self._connect_websocket()
    
    def send_websocket_message(self, message):
        """Send message through WebSocket"""
        with self.lock:
            if not self.ws or not self.ws_connected:
                raise Exception("WebSocket not connected")
            self.ws.send(message)
    
    def close_websocket(self):
        """Close WebSocket connection"""
        self.running = False
        with self.lock:
            if self.ws:
                try:
                    self.ws.close()
                except:
                    pass
                self.ws = None
                self.ws_connected = False
    
    def is_websocket_connected(self):
        """Return current WebSocket connection status"""
        with self.lock:
            return self.ws_connected
    

    
    # 基础模块
    def get_symbol_list(self):
        return self._get("/symbol/list", {})
    
    def get_symbol_holidays(self):
        return self._get("/symbol/holidays", {})
    
    # 股票模块
    def get_stock_info(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/stock/info", params)
    
    def get_stock_ipo(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/stock/ipo", params)
    
    def get_stock_split(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/stock/split", params)
    
    def get_stock_tick(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/stock/tick", params)
    
    def get_stock_quote(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/stock/quote", params)
    
    def get_stock_depth(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/stock/depth", params)
    
    def get_stock_kline(self, region, code, period, limit, end=None):
        params = {
            "region": region,
            "code": code,
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/stock/kline", params)
    
    def get_stock_ticks(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/stock/ticks", params)
    
    def get_stock_quotes(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/stock/quotes", params)
    
    def get_stock_depths(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/stock/depths", params)
    
    def get_stock_klines(self, region, codes, period, limit, end=None):
        params = {
            "region": region,
            "codes": ",".join(codes),
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/stock/klines", params)
    
    def connect_stock_websocket(self):
        self.connect_websocket("/websocket/stock")
    
    # 指数模块
    def get_indices_tick(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/indices/tick", params)
    
    def get_indices_quote(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/indices/quote", params)
    
    def get_indices_depth(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/indices/depth", params)
    
    def get_indices_kline(self, region, code, period, limit, end=None):
        params = {
            "region": region,
            "code": code,
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/indices/kline", params)
    
    def get_indices_ticks(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/indices/ticks", params)
    
    def get_indices_quotes(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/indices/quotes", params)
    
    def get_indices_depths(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/indices/depths", params)
    
    def get_indices_klines(self, region, codes, period, limit, end=None):
        params = {
            "region": region,
            "codes": ",".join(codes),
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/indices/klines", params)
    
    def connect_indices_websocket(self):
        self.connect_websocket("/websocket/indices")
    
    # 期货模块
    def get_future_tick(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/future/tick", params)
    
    def get_future_quote(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/future/quote", params)
    
    def get_future_depth(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/future/depth", params)
    
    def get_future_kline(self, region, code, period, limit, end=None):
        params = {
            "region": region,
            "code": code,
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/future/kline", params)
    
    def get_future_ticks(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/future/ticks", params)
    
    def get_future_quotes(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/future/quotes", params)
    
    def get_future_depths(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/future/depths", params)
    
    def get_future_klines(self, region, codes, period, limit, end=None):
        params = {
            "region": region,
            "codes": ",".join(codes),
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/future/klines", params)
    
    def connect_future_websocket(self):
        self.connect_websocket("/websocket/future")
    
    # 基金模块
    def get_fund_tick(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/fund/tick", params)
    
    def get_fund_quote(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/fund/quote", params)
    
    def get_fund_depth(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/fund/depth", params)
    
    def get_fund_kline(self, region, code, period, limit, end=None):
        params = {
            "region": region,
            "code": code,
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/fund/kline", params)
    
    def get_fund_ticks(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/fund/ticks", params)
    
    def get_fund_quotes(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/fund/quotes", params)
    
    def get_fund_depths(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/fund/depths", params)
    
    def get_fund_klines(self, region, codes, period, limit, end=None):
        params = {
            "region": region,
            "codes": ",".join(codes),
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/fund/klines", params)
    
    def connect_fund_websocket(self):
        self.connect_websocket("/websocket/fund")
    
    # 外汇模块
    def get_forex_tick(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/forex/tick", params)
    
    def get_forex_quote(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/forex/quote", params)
    
    def get_forex_depth(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/forex/depth", params)
    
    def get_forex_kline(self, region, code, period, limit, end=None):
        params = {
            "region": region,
            "code": code,
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/forex/kline", params)
    
    def get_forex_ticks(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/forex/ticks", params)
    
    def get_forex_quotes(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/forex/quotes", params)
    
    def get_forex_depths(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/forex/depths", params)
    
    def get_forex_klines(self, region, codes, period, limit, end=None):
        params = {
            "region": region,
            "codes": ",".join(codes),
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/forex/klines", params)
    
    def connect_forex_websocket(self):
        self.connect_websocket("/websocket/forex")
    
    # 加密货币模块
    def get_crypto_tick(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/crypto/tick", params)
    
    def get_crypto_quote(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/crypto/quote", params)
    
    def get_crypto_depth(self, region, code):
        params = {"region": region, "code": code}
        return self._get("/crypto/depth", params)
    
    def get_crypto_kline(self, region, code, period, limit, end=None):
        params = {
            "region": region,
            "code": code,
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/crypto/kline", params)
    
    def get_crypto_ticks(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/crypto/ticks", params)
    
    def get_crypto_quotes(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/crypto/quotes", params)
    
    def get_crypto_depths(self, region, codes):
        params = {"region": region, "codes": ",".join(codes)}
        return self._get("/crypto/depths", params)
    
    def get_crypto_klines(self, region, codes, period, limit, end=None):
        params = {
            "region": region,
            "codes": ",".join(codes),
            "period": period,
            "limit": limit
        }
        if end:
            params["end"] = end
        return self._get("/crypto/klines", params)
    
    def connect_crypto_websocket(self):
        self.connect_websocket("/websocket/crypto")
