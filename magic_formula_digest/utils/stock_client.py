from requests import get
from requests.exceptions import RequestException
import json
import logging
from time import sleep
from pathlib import Path
from utils.config import ALPHA_VANTAGE_API_KEY

# Configure logging
logging.basicConfig(
    filename='data/error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def fetch_stock_data(ticker):
    base_url = 'https://www.alphavantage.co/query'
    params = {'apikey': ALPHA_VANTAGE_API_KEY}

    # Fetch OVERVIEW data
    overview_data = None
    for attempt in range(3):
        try:
            response = get(
                base_url,
                params={**params, 'function': 'OVERVIEW', 'symbol': ticker},
            )
            response.raise_for_status()
            overview_data = response.json()
            break
        except RequestException as e:
            logging.error(f'Failed to fetch OVERVIEW data for {ticker}: {e}')
            if attempt < 2:
                sleep(2)  # Wait before retrying

    # Fetch TIME_SERIES_DAILY data
    time_series_data = None
    for attempt in range(3):
        try:
            response = get(
                base_url,
                params={**params, 'function': 'TIME_SERIES_DAILY', 'symbol': ticker},
            )
            response.raise_for_status()
            time_series_data = response.json()
            break
        except RequestException as e:
            logging.error(f'Failed to fetch TIME_SERIES_DAILY data for {ticker}: {e}')
            if attempt < 2:
                sleep(2)  # Wait before retrying

    # Save raw data to file
    if overview_data and time_series_data:
        raw_data = {'OVERVIEW': overview_data, 'TIME_SERIES_DAILY': time_series_data}
        raw_file = Path(f'data/raw_stocks/{ticker}.json')
        raw_file.parent.mkdir(parents=True, exist_ok=True)
        with open(raw_file, 'w') as f:
            json.dump(raw_data, f, indent=4)

    return overview_data, time_series_data
