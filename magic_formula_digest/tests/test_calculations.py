import unittest
from unittest.mock import patch
from utils.processor import calculate_earnings_yield, calculate_roc
from utils.news_client import filter_news

class TestCalculations(unittest.TestCase):
    def test_earnings_yield(self):
        # Test earnings yield calculation
        ebit = 1000000
        enterprise_value = 5000000
        expected_yield = 0.2  # 20%
        self.assertAlmostEqual(calculate_earnings_yield(ebit, enterprise_value), expected_yield)

        # Test edge case with zero enterprise value
        with self.assertRaises(ValueError):
            calculate_earnings_yield(ebit, 0)

    def test_roc(self):
        # Test ROC calculation
        ebit = 500000
        net_fixed_assets = 2000000
        working_capital = 500000
        expected_roc = 0.2  # 20%
        self.assertAlmostEqual(calculate_roc(ebit, net_fixed_assets, working_capital), expected_roc)

        # Test edge case with zero denominator
        with self.assertRaises(ValueError):
            calculate_roc(ebit, 0, 0)

    def test_news_filtering(self):
        # Test news filtering logic
        test_articles = [
            {"source": {"name": "CNN"}, "title": "Market Update"},
            {"source": {"name": "Unknown Blog"}, "title": "Random Thoughts"},
            {"source": {"name": "Reuters"}, "title": "Economic Report"},
            {"source": {"name": "Bloomberg"}, "title": "Stock Analysis"},
            {"source": {"name": "Random Site"}, "title": "Investment Tips"}
        ]
        
        expected_filtered = [
            {"source": {"name": "CNN"}, "title": "Market Update"},
            {"source": {"name": "Reuters"}, "title": "Economic Report"},
            {"source": {"name": "Bloomberg"}, "title": "Stock Analysis"}
        ]
        
        filtered_articles = filter_news(test_articles)
        self.assertEqual(filtered_articles, expected_filtered)
        
        # Test empty input
        self.assertEqual(filter_news([]), [])

if __name__ == "__main__":
    unittest.main()
