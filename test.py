import time
import pyupbit
import datetime

access = ""
secret = ""

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

def auto_trade_start(ticker) :
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(ticker)
        end_time = start_time + datetime.timedelta(minutes=240)
        print(f"{now} : 오토트레이딩 진행중...")

        if start_time < now < (end_time - datetime.timedelta(seconds=10)):
            target_price = get_target_price(ticker, 0.5)
            current_price = get_current_price(ticker)
            print(f"{now} : 매수가능한 코인 탐색중...")
            if target_price < current_price:
                krw = int(get_balance("KRW"))
                if krw > 5000:
                    upbit.buy_market_order(ticker, krw*0.9995)
                    print(f"{now} : {ticker}에 대한 매수주문을 넣었습니다.")

        else:
            ticker_balance = get_balance(ticker[4:])
            print(f"{now} : 봉이 마감되어 남은 코인을 매도합니다.")
            if ticker_balance > 0.00008:
                upbit.sell_market_order(ticker, ticker_balance*0.9995)
                print(f"{now} : {ticker}에 대한 매도주문을 넣었습니다.")

        time.sleep(1)

    except Exception as e:
        print(e)
        print(f"{now} : 오류가 발생하였습니다.")
        time.sleep(1)

while True :
    try :
        auto_trade_start("KRW-BTC")
        time.sleep(1)
        auto_trade_start("KRW-ETH")
        time.sleep(1)
        auto_trade_start("KRW-DOGE")
        time.sleep(1)
        auto_trade_start("KRW-ETC")
        time.sleep(1)
        auto_trade_start("KRW-XRP")
        time.sleep(1)

    except :
        pass
