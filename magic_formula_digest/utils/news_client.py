import requests
import csv
from datetime import datetime
from pathlib import Path
import logging
from utils.config import NEWS_API_KEY

# Configure logging
logging.basicConfig(
    filename='data/error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def fetch_news(ticker: str):
    '''Fetch news headlines for a stock ticker using NewsAPI.'''
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': ticker,
        'sources': 'bloomberg,reuters,cnbc,marketwatch',
        'apiKey': NEWS_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('articles', [])
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to fetch news for {ticker}: {e}')
        return []

def save_news(ticker: str, news: list, output_dir: str = 'data/processed'):
    '''Save relevant news to a CSV file.'''
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime('%Y%m%d')
    output_file = output_dir / f'news_{date_str}.csv'

    with open(output_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Ticker', 'Headline', 'Source', 'URL'])
        if not output_file.exists():
            writer.writeheader()
        for article in news:
            writer.writerow({
                'Ticker': ticker,
                'Headline': article['title'],
                'Source': article['source']['name'],
                'URL': article['url'],
            })
