import pytz
import datetime
from dhanhq import dhanhq


class DhanHQClient:
    def __init__(self, client_id: str, access_token: str):
        try:
            self.dhan = dhanhq(client_id, access_token)
            self.ist = pytz.timezone('Asia/Kolkata')
        except Exception as e:
            raise ConnectionError(f"Failed to initialize DhanHQ client: {e}")

    def get_live_price(self, securities):
        """
        Fetch live prices for multiple stocks.
        `securities` should be a list of dictionaries.
        Each dictionary should have 'security_id', 'exchange_segment', and 'instrument_type'.
        """
        try:
            if not isinstance(securities, list):
                return False

            formatted_responses = {}
            for stock in securities:
                response = self._fetch_and_format_price(stock)
                response = self._get_time_and_close_prices(response)
                formatted_responses[stock.security_id] = response

            print(f'formatted_responses {formatted_responses}')

            return formatted_responses
        except Exception as e:
            return False

    def _fetch_and_format_price(self, stock):
        """
        Fetches the live price and formats the time for a single stock.
        Handles the case when the market is closed or no data is available.
        """
        try:
            response = self.dhan.intraday_minute_data(
                security_id=stock.security_id,
                exchange_segment=stock.exchange_segment,
                instrument_type=stock.instrument_type
            )

            # Ensure response is a dictionary
            if not isinstance(response, dict):
                return False

            # Check if 'data' is present and has 'start_Time'
            if 'data' not in response or response['data'] == '':
                return False

            # Check if the response indicates failure
            if response.get('status') == 'failure':
                return False

            # Proceed to format the timestamps
            return self._format_time_from_unix_to_ist(response)
        except Exception as e:
            return False

    def _fetch_and_format_close_price(self, stock):
        """
        Fetches the live price and formats the time for a single stock.
        Handles the case when the market is closed or no data is available.
        """
        try:

            # GET TODAT DATE
            today = datetime.date.today()
            print(f'today {today}')

            # GET 10 DAYS BEFORE DATE
            ten_days_before = today - datetime.timedelta(days=10)
            print(f'ten_days_before {ten_days_before}')

            print(f'stock {stock}')
            response = self.dhan.historical_daily_data(
                symbol=stock.symbol,
                exchange_segment=stock.exchange_segment,
                instrument_type=stock.instrument_type,
                expiry_code=0,
                from_date=str(ten_days_before),
                to_date=str(today),
            )

            print(f'response000 {response}')

            # Ensure response is a dictionary
            if not isinstance(response, dict):
                return {
                    'message': f"Unexpected response for {stock.security_id}: {response}"
                }

            # Check if 'data' is present and has 'start_Time'
            if 'data' not in response or response['data'] == '':
                return {
                    'message': f"No data available for {stock.security_id}. Market might be closed or data not available."
                }

            # Check if the response indicates failure
            if response.get('status') == 'failure':
                return {
                    'message': f"Failed to fetch data for {stock.security_id}: {response['remarks']['message']}"
                }

            # Proceed to format the timestamps
            return self._format_time_from_unix_to_ist(response)
        except KeyError as e:
            raise ValueError(f"Missing required stock information: {e}")
        except Exception as e:
            raise RuntimeError(
                f"Error while fetching live price for {stock.security_id}: {e}"
            )

    def _format_time_from_unix_to_ist(self, response):
        """
        Format the timestamps from UNIX to IST.
        """
        try:
            ist_times = []
            for timestamp in response['data']['start_Time']:
                timestamp = float(timestamp)
                utc_time = datetime.datetime.utcfromtimestamp(timestamp)
                ist_time = utc_time.replace(
                    tzinfo=pytz.utc).astimezone(self.ist)
                ist_times.append(ist_time.strftime('%Y-%m-%d %H:%M:%S %Z %z'))

            response['data']['start_Time'] = ist_times
            return response
        except Exception as e:
            return False

    def _get_time_and_close_prices(self, stock_data):
        """
        Extract time and corresponding close prices from the stock data.
        The input stock_data should contain 'start_Time' and 'close' lists.
        Returns a dictionary where each timestamp maps to the close price.
        """
        try:
            print(stock_data)
            times = stock_data['data']['start_Time']
            close_prices = stock_data['data']['close']

            if not times or not close_prices:
                raise ValueError(
                    "Missing 'start_Time' or 'close' data in response.")

            if len(times) != len(close_prices):
                raise ValueError(
                    "The lengths of 'start_Time' and 'close' do not match.")

            # Create a dictionary of time -> close price
            time_to_close_price = {time: close for time,
                                   close in zip(times, close_prices)}
            return time_to_close_price
        except KeyError as e:
            raise ValueError(f"Missing required data: {e}")
        except Exception as e:
            raise RuntimeError(f"Error processing time and close prices: {e}")

    def get_close_price(self, securities):
        """
        Fetch close prices for multiple stocks.
        `securities` should be a list of dictionaries.
        Each dictionary should have 'security_id', 'exchange_segment', and 'instrument_type'.
        """
        try:
            if not isinstance(securities, list):
                raise TypeError(
                    "Input should be a list of dictionaries representing stocks."
                )

            formatted_responses = {}
            for stock in securities:
                response = self._fetch_and_format_close_price(stock)
                print(f'response {response}')
                response = self._get_time_and_close_prices(response)
                formatted_responses[stock.security_id] = response

            print(f'formatted_responses {formatted_responses}')

            return formatted_responses
        except TypeError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Failed to fetch live price data: {e}")
