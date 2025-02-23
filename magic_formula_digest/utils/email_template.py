from datetime import datetime, timedelta
import sqlite3
from typing import List, Dict
from pathlib import Path

def fetch_top_stocks(db_path: str = 'data/history.db') -> List[Dict]:
    '''Fetch the top 10 stocks from the SQLite database.'''
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ticker, earnings_yield, roc, rank
            FROM stock_rankings
            WHERE date = (SELECT MAX(date) FROM stock_rankings)
            ORDER BY rank
            LIMIT 10
        ''')
        return [
            {'ticker': row[0], 'earnings_yield': row[1], 'roc': row[2], 'rank': row[3]}
            for row in cursor.fetchall()
        ]

def fetch_consistency(ticker: str, db_path: str = 'data/history.db') -> int:
    '''Fetch the number of days a stock has been in the top 10.'''
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(DISTINCT date)
            FROM stock_rankings
            WHERE ticker = ? AND rank <= 10
        ''', (ticker,))
        return cursor.fetchone()[0]

def generate_email_content() -> tuple[str, str]:
    '''Generate plain text and HTML email content for the top 10 stocks.'''
    top_stocks = fetch_top_stocks()
    email_text = 'Top 10 Stocks Today:\n\n'
    email_html = '''
        <h1>Top 10 Stocks Today</h1>
        <table border='1'>
            <tr>
                <th>Ticker</th>
                <th>Earnings Yield</th>
                <th>ROC</th>
                <th>Why This Stock?</th>
                <th>News</th>
            </tr>
    '''

    for stock in top_stocks:
        consistency = fetch_consistency(stock['ticker'])
        why_stock = f'High ROC of {stock['roc']:.1f}%'
        recommendation = f'Ranked top 10 for {consistency} days'

        # Fetch news headlines
        news = fetch_news(stock['ticker'])
        news_text = '\n'.join(f'- {article['title']} ({article['source']['name']})' for article in news)
        news_html = '<ul>' + ''.join(
            f'<li>{article['title']} (<a href='{article['url']}'>{article['source']['name']}</a>)</li>'
            for article in news
        ) + '</ul>'

        # Add to email content
        email_text += f'''
            Ticker: {stock['ticker']}
            Earnings Yield: {stock['earnings_yield']:.2f}
            ROC: {stock['roc']:.2f}%
            Why This Stock?: {why_stock}
            Recommendation: {recommendation}
            News:
            {news_text}
            \n
        '''
        email_html += f'''
            <tr>
                <td>{stock['ticker']}</td>
                <td>{stock['earnings_yield']:.2f}</td>
                <td>{stock['roc']:.2f}%</td>
                <td>{why_stock}<br>{recommendation}</td>
                <td>{news_html}</td>
            </tr>
        '''

    email_html += '</table>'
    return email_text, email_html
