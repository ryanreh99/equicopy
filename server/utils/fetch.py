import requests
from pandas import read_csv
from datetime import timedelta

from django.utils import timezone


def get_formatted_date(days = 0):
    today = timezone.now() - timedelta(days)
    weekday = today.weekday()

    if weekday > 4:
        # No data available for saturday (5) and sunday (6)
        # So, fetch for friday's (4) data. 
        today -= timedelta(weekday - 4)

    return today.strftime('%d%m%y')

def get_dataframe(csv_file):
    return read_csv(
        csv_file,
        index_col='SC_CODE'
    )

def get_url(fetch_date):
    return f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{fetch_date}_CSV.ZIP'

def get_response(fetch_date):
    url = get_url(fetch_date)
    headers = { 'User-Agent': 'Mozilla/5.0' }
    return requests.get(
        url,
        headers=headers,
        stream=True
    )
