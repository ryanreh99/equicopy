import requests
from pandas import read_csv
from datetime import date, timedelta

def get_formatted_date():
    today = date.today()
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

def get_response(fetch_date):
    url = f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{fetch_date}_CSV.ZIP'
    headers = { 'User-Agent': 'Mozilla/5.0' }
    return requests.get(
        url,
        headers=headers,
        stream=True
    )
