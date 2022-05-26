import os

TICKER = os.getenv('TICKER', 'IBM')
API_KEY = os.getenv('API_KEY')
REDIS = os.getenv('REDIS', 'localhost')
URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'