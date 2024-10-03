from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from api.endpoints.sdk.dhanhq import DhanHQClient
from config import settings
import logging
from fastapi import APIRouter

router = APIRouter()


# Define the structure of the incoming data using Pydantic models

class Security(BaseModel):
    security_id: str
    exchange_segment: str
    instrument_type: str


class SecuritiesPayload(BaseModel):
    securities: List[Security]


router = APIRouter()


@router.post("/get-stocks-ohlc", tags=["Get Stocks OHLC"])
def get_stocks_data(payload: SecuritiesPayload):
    try:
        # Initialize DhanHQ client
        dhan_client = DhanHQClient(
            settings.DHANHQ_CLIENT_ID, settings.DHANHQ_ACCESS_TOKEN)

        # Extract the list of securities from the payload
        multiple_stocks = payload.securities

        print(multiple_stocks)

        # Fetch live prices for multiple stocks
        multiple_stock_prices = dhan_client.get_live_price(multiple_stocks)

        # Log the result for debugging purposes
        logging.info(f"Fetched Multiple Stock Prices: {multiple_stock_prices}")

        # Return stock prices in a structured format for the frontend
        return {
            "status": "success",
            "data": multiple_stock_prices
        }
    except Exception as e:
        logging.error(f"Error fetching stock OHLC data: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to fetch stock data")


# @router.post("/get-stocks-ohlc", tags=["Get Stocks OHLC"])
# def get_stocks_data():
#     try:
#         dhan_client = DhanHQClient(
#             settings.DHANHQ_CLIENT_ID, settings.DHANHQ_ACCESS_TOKEN)

#         # print("Dhan Client: ", dhan_client)
#         # # Fetch live price for a single stock
#         # single_stock = {'security_id': '500008',
#         #                 'exchange_segment': 'BSE_EQ', 'instrument_type': 'EQUITY'}
#         # print(f'Single Stock: {single_stock}')
#         # single_stock_price = dhan_client.get_live_price(single_stock)
#         # print(f'Single Stock Price: {single_stock_price}')

#         # Fetch live prices for multiple stocks
#         multiple_stocks = [
#             {'security_id': '500008', 'exchange_segment': 'BSE_EQ',
#                 'instrument_type': 'EQUITY'},
#             {'security_id': '500009', 'exchange_segment': 'BSE_EQ',
#                 'instrument_type': 'EQUITY'}
#         ]

#         multiple_stock_prices = dhan_client.get_live_price(multiple_stocks)
#         print(f'Multiple Stock Prices: {multiple_stock_prices}')
#         return multiple_stock_prices
#     except Exception as e:
#         logging.error(f"Main Health :{str(e)}")
#         raise e
