import time
import hmac
import hashlib
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")
BASE_URL = "https://api.bitget.com"

symbol = "BTCUSDT_UMCBL"
marginCoin = "USDT"

def get_timestamp():
    return str(int(time.time() * 1000))

def sign(method, path, timestamp, body=""):
    pre_hash = f"{timestamp}{API_KEY}{method.upper()}{path}{body}"
    signature = hmac.new(API_SECRET.encode(), pre_hash.encode(), hashlib.sha256).hexdigest()
    return signature

def get_headers(method, path, body=""):
    timestamp = get_timestamp()
    signature = sign(method, path, timestamp, body)
    return {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json"
    }

def get_balance():
    path = f"/api/mix/v1/account/account?symbol={symbol}&marginCoin={marginCoin}"
    url = BASE_URL + path
    headers = get_headers("GET", f"/api/mix/v1/account/account?symbol={symbol}&marginCoin={marginCoin}")
    res = requests.get(url, headers=headers)
    try:
        data = res.json()
        print("🔍 Balance brut :", data)
        return float(data["data"]["available"])
    except Exception as e:
        print("❌ Erreur lecture balance :", res.text)
        return 0

def place_order():
    path = "/api/mix/v1/order/placeOrder"
    url = BASE_URL + path
    body = {
        "symbol": symbol,
        "marginCoin": marginCoin,
        "side": "open_long",
        "orderType": "limit",
        "price": "120000",
        "size": "0.0001",
        "timeInForceValue": "normal"
    }
    body_json = json.dumps(body, separators=(',', ':'))
    headers = get_headers("POST", path, body_json)
    res = requests.post(url, headers=headers, data=body_json)
    print("📤 Résultat ordre :", res.json())

# === Execution ===
get_balance()
place_order()
