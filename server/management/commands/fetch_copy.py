import io
import redis
import requests
import pandas as pd
from datetime import date
from zipfile import ZipFile

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Fetches the BhavCopy and mass inserts data'

    def handle(self, *args, **options):
        today = date.today()
        fetch_date = today.strftime('%d%m%y')
        print("Fetching date:", fetch_date)

        url = f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{fetch_date}_CSV.ZIP'
        headers = { 'User-Agent': 'Mozilla/5.0' }
        response = requests.get(url, headers=headers, stream=True)

        zip_file = ZipFile(io.BytesIO(response.content))
        filename = zip_file.open(f'EQ{fetch_date}.CSV')

        df = pd.read_csv(filename, index_col='SC_CODE')

        CHUNK_SIZE = 500
        BATCH_START = 0
        ORDER_NUM = 0
        NUM_ENTRIES = df.shape[0]

        rclient = redis.Redis(
            host='localhost',
            port=6379,
            db=0
        )

        def clean(item):
            if isinstance(item, str):
                return item.strip()
            return item
        
        def mass_insert(items: dict, keys: list, order_num: int):           
            [
                pipe.zadd("order", { str(key): order_num + index })
                for index, key in enumerate(keys)
            ]

            [
                pipe.hset(
                    clean(hashname),
                    clean(field),
                    clean(items[field][hashname])
                )
                for field in items
                for hashname in items[field]
            ]

            return order_num + len(keys)

        with rclient.pipeline() as pipe:
            while BATCH_START <= NUM_ENTRIES:
                items = df[BATCH_START : BATCH_START + CHUNK_SIZE]
                keys = items.index.values
                ORDER_NUM = mass_insert(items.to_dict(), keys, ORDER_NUM)
                BATCH_START += CHUNK_SIZE
            pipe.execute()


        self.stdout.write(self.style.SUCCESS('Successfully inserted data!'))
