from pydantic import BaseModel
from typing import List, Union


class AssetBalance(BaseModel):
    asset: str
    balance: str


class AccountInfo(BaseModel):
    uid: int
    account_type: str
    btc_balance: AssetBalance
    usdt_balance: AssetBalance
    eth_balance: AssetBalance


class PriceInfo(BaseModel):
    symbol: str
    price: str


class CandleInfo(BaseModel):
    open_time: Union[str, int]
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time: Union[str, int]
    quote_asset_volume: float
    number_of_trades: int
    taker_buy_base_asset_volume: float
    taker_buy_quote_asset_volume: float
    ignore: str


class OrderRequest(BaseModel):
    symbol: str
    side: str
    order_type: str
    quantity: float
    test: bool = True


class OrderFill(BaseModel):
    price: str
    qty: str
    commission: str
    commissionAsset: str
    tradeId: int


class Order(BaseModel):
    symbol: str
    orderId: int
    clientOrderId: str
    transactTime: int
    price: str
    origQty: str
    executedQty: str
    origQuoteOrderQty: str
    cummulativeQuoteQty: str
    status: str
    timeInForce: str
    type: str
    side: str
    workingTime: int
    fills: List[OrderFill]
    selfTradePreventionMode: str
class Trades(BaseModel):
    symbol: str
    id: int
    orderId: int
    price: str
    qty: str
    quoteQty: str
    comission: str
    comissionAsset: str
    time: int
    isBuyer: bool
    isMaker: bool
    bestatch: bool
