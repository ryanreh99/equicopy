from io import BytesIO
from zipfile import ZipFile, BadZipFile

from django.core.management.base import BaseCommand, CommandError

from server.utils.fetch import get_formatted_date, get_dataframe, get_response
from server.utils.redis import redis_api


class Command(BaseCommand):
    help = 'Fetches the BhavCopy and mass inserts the data'

    def insert_into_redis(self, df):
        redis_api.flushall()

        CHUNK_SIZE = 500
        BATCH_START = 0
        ORDER_NUM = 0
        NUM_ENTRIES = df.shape[0]

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

        with redis_api.get_pipeline() as pipe:
            while BATCH_START <= NUM_ENTRIES:
                items = df[BATCH_START : BATCH_START + CHUNK_SIZE]
                keys = items.index.values
                ORDER_NUM = mass_insert(items.to_dict(), keys, ORDER_NUM)
                BATCH_START += CHUNK_SIZE
            pipe.execute()


    def handle(self, *args, **options):
        fetch_date = get_formatted_date()
        print("Fetching date:", fetch_date)

        response = get_response(fetch_date)

        try:
            zip_file = ZipFile(BytesIO(response.content))
        except BadZipFile:
            self.stdout.write(self.style.WARNING("ERROR: Incorrect file received"))
            return
        csv_file = zip_file.open(f'EQ{fetch_date}.CSV')

        df = get_dataframe(csv_file)
        self.insert_into_redis(df)

        self.stdout.write(self.style.SUCCESS('Successfully inserted data!'))
