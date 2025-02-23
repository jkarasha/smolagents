import logging
import json
import argparse
from utils.stock_client import fetch_stock_data
from utils.processor import process_stock_data, save_ranked_stocks
from utils.news_client import fetch_news, save_news
from utils.email_sender import send_daily_digest, generate_email_content
from utils.config import TO_EMAIL

# Configure logging
logging.basicConfig(
    filename="data/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def load_mock_data():
    """Load mock data from test fixtures"""
    with open("tests/fixtures/mock_stocks.json", "r") as f:
        stocks = json.load(f)
    with open("tests/fixtures/mock_news.json", "r") as f:
        news = json.load(f)
    return stocks, news

def run_test_mode():
    """Run the application in test mode using mock data"""
    logging.info("Running in test mode")
    
    # Load mock data
    stocks, news_data = load_mock_data()
    
    # Generate email content
    subject, body = generate_email_content(stocks, news_data)
    
    # Save test email output
    with open("tests/output/test_email.html", "w") as f:
        f.write(body)
    
    logging.info("Test email saved to tests/output/test_email.html")
    return True

def run_production_mode():
    """Run the application in production mode"""
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    stocks = {}

    # Fetch and process stock data
    for ticker in tickers:
        try:
            overview, time_series = fetch_stock_data(ticker)
            processed_data = process_stock_data(ticker, overview, time_series)
            if processed_data:
                stocks[ticker] = processed_data
        except Exception as e:
            logging.error(f"Failed to fetch or process data for {ticker}: {e}")

    # Save ranked stocks
    try:
        save_ranked_stocks(stocks)
        logging.info("Successfully saved ranked stocks.")
    except Exception as e:
        logging.error(f"Failed to save ranked stocks: {e}")

    # Fetch news for top 10 stocks
    top_tickers = [stock["Ticker"] for stock in sorted(stocks.values(), key=lambda x: x["Rank"])[:10]]
    for ticker in top_tickers:
        try:
            news = fetch_news(ticker)
            save_news(ticker, news)
        except Exception as e:
            logging.error(f"Failed to fetch or save news for {ticker}: {e}")

    # Send daily digest email
    try:
        if send_daily_digest(TO_EMAIL):
            logging.info("Successfully sent daily digest email.")
            return True
        else:
            logging.error("Failed to send daily digest email.")
            return False
    except Exception as e:
        logging.error(f"Failed to send daily digest email: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Stock Analysis Tool")
    parser.add_argument("--test", action="store_true", help="Run in test mode using mock data")
    args = parser.parse_args()
    
    if args.test:
        return run_test_mode()
    else:
        return run_production_mode()

if __name__ == "__main__":
    main()