import asyncio
import websockets
import json
import ssl
import certifi
import datetime

datetime.datetime.today().timestamp()

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

END_DATE = datetime.datetime.today()
END_DATE = END_DATE.replace(minute=10)
START_DATE = END_DATE - datetime.timedelta(minutes=1)


print(f'start date is {START_DATE.isoformat()}, end date is {END_DATE.isoformat()}')


msg = \
{
  "jsonrpc" : "2.0",
  "id" : 8387,
  "method" : "public/get_historical_volatility",
  "params" : {
    "currency" : "BTC"
  }
}

msg = \
{
  "id" : 1,
  "method" : "public/get_mark_price_history",
  "params" : {
    "instrument_name" : "ETH-10JAN25-3000-C", #"BTC-28MAR25-150000-C",
    "start_timestamp" : str(int(START_DATE.timestamp()*1e3)),
    "end_timestamp" : str(int(END_DATE.timestamp()*1e3)),
  },
  "jsonrpc" : "2.0"
}

async def call_api(msg):
   async with websockets.connect(uri='wss://test.deribit.com/ws/api/v2', ssl=ssl_context) as websocket:
       await websocket.send(msg)
       while True:
           response = await websocket.recv()
           # do something with the response...
           print(response)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
