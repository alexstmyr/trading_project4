from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from dotenv import load_dotenv
from pydantic import parse_obj_as

from client import BinanceTestClient
from models import AccountInfo, OrderRequest, PriceInfo, CandleInfo, Trades

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
client = BinanceTestClient(api_key, api_secret)


@app.get("/api/health")
async def health():
    return {"message": "OK"}

@app.get('/api/binance-health')
async def binance_health():
    """
    Get Binance API status

    """
    if client.ping():
        return {'status': 'Binance API is reachable'}
    raise HTTPException(status_code = 503, detail = 'Binance API is not reachable')

@app.get("/api/account", response_model=AccountInfo)
async def get_account() -> AccountInfo:
    """
    Get Binance account information
    """
    try:
        info = client.get_account_info()
        balances = {bal['asset']: bal for bal in info['balances']}

        def get_balance(asset: str):
            if asset in balances:
                return {"asset": asset, "balance": balances[asset].get("free", "0")}
            return None

        return {
            "uid": info.get("accountNumber", 0),
            "account_type": info.get("accountType", "SPOT"),
            "btc_balance": get_balance("BTC"),
            "usdt_balance": get_balance("USDT"),
            "eth_balance": get_balance("ETH")
        }
    except Exception as e:

        print(f'Error al obtener cuenta: {e}')
        raise HTTPException(status_code = 500, detail = str(e))


@app.get("/api/price")
async def get_price(symbol: str):
    """
    Get price of a symbol
    """
    try:
        price = client.get_price(symbol)
        return PriceInfo(**price)
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))


@app.get("/api/price-history")
async def get_price(symbol: str, interval: str = '1h'):
    """
    Get price of a symbol
    """
    try:
        raw_candles = client.get_price_history(symbol, interval)

        keys = [
            "open_time", "open", "high", "low", "close", "volume", "close_time",
            "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume", "ignore"
        ]

        dict_candels = [dict(zip(keys,c)) for c in raw_candles]

        candles = parse_obj_as(list[CandleInfo], dict_candels)

        return candles
    except Exception as e:
        print(f'Error en price history: {e}')
        raise HTTPException(status_code = 500, detail = str(e))


@app.post("/api/order")
async def create_order(order: OrderRequest):
    """
    Create a Binance order
    """
    try:
        result = client.place_order(
            symbol=order.symbol,
            side = order.side,
            order_type=order.order_type,
            quantity=order.quantity,
            test = order.test
        )
        return {'status': 'Order submitted!', 'response': result}
    except Exception as e:
        raise HTTPException(status_code = 500, detail =str(e))

