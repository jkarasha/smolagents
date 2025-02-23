from pathlib import Path
import csv
from datetime import datetime
from typing import Dict, Optional, List
import sqlite3

def compute_earnings_yield(ebit: float, enterprise_value: float) -> Optional[float]:
    '''Compute earnings yield (EBIT / Enterprise Value).'''
    if enterprise_value <= 0:
        return None
    return ebit / enterprise_value

def compute_roc(ebit: float, net_fixed_assets: float, working_capital: float) -> Optional[float]:
    '''Compute return on capital (EBIT / (Net Fixed Assets + Working Capital)).'''
    denominator = net_fixed_assets + working_capital
    if denominator <= 0:
        return None
    return ebit / denominator

def process_stock_data(ticker: str, overview: Dict, time_series: Dict) -> Optional[Dict]:
    '''Process stock data to compute metrics.'''
    try:
        ebit = float(overview.get('EBIT', 0))
        enterprise_value = float(overview.get('EnterpriseValue', 0))
        net_fixed_assets = float(overview.get('NetFixedAssets', 0))
        working_capital = float(overview.get('WorkingCapital', 0))
        latest_close = float(list(time_series['Time Series (Daily)'].values())[0]['4. close'])
        prev_close = float(list(time_series['Time Series (Daily)'].values())[1]['4. close'])
        pct_change = (latest_close - prev_close) / prev_close * 100

        earnings_yield = compute_earnings_yield(ebit, enterprise_value)
        roc = compute_roc(ebit, net_fixed_assets, working_capital)

        if earnings_yield is None or roc is None or earnings_yield < 0 or roc < 0:
            return None

        return {
            'Ticker': ticker,
            'Price': latest_close,
            'PctChange': pct_change,
            'EarningsYield': earnings_yield,
            'ROC': roc,
        }
    except (KeyError, ValueError):
        return None

def rank_stocks(stocks: Dict[str, Dict]) -> List[Dict]:
    '''Rank stocks by earnings yield and return on capital.'''
    ranked_stocks = sorted(
        [stock for stock in stocks.values() if stock],
        key=lambda x: (x['EarningsYield'], x['ROC']),
        reverse=True,
    )
    for rank, stock in enumerate(ranked_stocks, start=1):
        stock['Rank'] = rank
    return ranked_stocks

def save_ranked_stocks(stocks: Dict[str, Dict], output_dir: str = 'data/processed'):
    '''Save processed stock data to a CSV file and SQLite database.'''
    ranked_stocks = rank_stocks(stocks)
    date_str = datetime.now().strftime('%Y%m%d')

    # Save to CSV
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f'ranked_stocks_{date_str}.csv'

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Ticker', 'Price', 'PctChange', 'EarningsYield', 'ROC', 'Rank'])
        writer.writeheader()
        writer.writerows(ranked_stocks)

    # Save to SQLite
    with sqlite3.connect('data/history.db') as conn:
        cursor = conn.cursor()
        cursor.executemany(
            '''
            INSERT INTO stock_rankings (date, ticker, earnings_yield, roc, rank)
            VALUES (?, ?, ?, ?, ?)
            ''',
            [
                (date_str, stock['Ticker'], stock['EarningsYield'], stock['ROC'], stock['Rank'])
                for stock in ranked_stocks
            ],
        )
        conn.commit()
