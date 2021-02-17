from io import BytesIO
from zipfile import ZipFile, BadZipFile

from django.core.management.base import BaseCommand, CommandError

from server.utils.fetch import (
    get_formatted_date,
    get_dataframe,
    get_response
)
from server.utils.redis import redis_api


class Command(BaseCommand):
    help = 'Fetches the BhavCopy and mass inserts the data'

    def insert_into_redis(self, df, fetch_date):
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
                pipe.zadd("order", { "stock:" + str(key): order_num + index })
                for index, key in enumerate(keys)
            ]

            [
                pipe.hset(
                    f"stock:{clean(hashname)}",
                    clean(field),
                    clean(items[field][hashname])
                )
                for field in items
                for hashname in items[field]
            ]

            return order_num + len(keys)

        with redis_api.get_pipeline() as pipe:
            pipe.set("date", fetch_date)

            while BATCH_START <= NUM_ENTRIES:
                items = df[BATCH_START : BATCH_START + CHUNK_SIZE]
                keys = items.index.values
                ORDER_NUM = mass_insert(
                    items.to_dict(),
                    keys,
                    ORDER_NUM
                )
                BATCH_START += CHUNK_SIZE
            pipe.execute()
        redis_api.create_index()


    def get_csv_file(self, days=0):
        # If current date data not found.
        # Try fetching previous days.
        fetch_date = get_formatted_date(days)
        print("Fetching date:", fetch_date)

        response = get_response(fetch_date)

        try:
            zip_file = ZipFile(BytesIO(response.content))
        except BadZipFile:
            return False, None, None
        csv_file = zip_file.open(f'EQ{fetch_date}.CSV')
        
        return True, csv_file, fetch_date

    def handle(self, *args, **options):
        MAX_RETRIES = 1
        RETRIES_LEFT = 1
        while (RETRIES_LEFT >= 0):
            success, csv_file, fetch_date = self.get_csv_file(
                MAX_RETRIES - RETRIES_LEFT
            )
            RETRIES_LEFT -= 1
            if success:
                break
        
        if not success:
            return self.stdout.write(
                self.style.WARNING("ERROR: Incorrect file received")
            )

        df = get_dataframe(csv_file)
        self.insert_into_redis(df, fetch_date)

        self.stdout.write(
            self.style.SUCCESS('Successfully inserted data!')
        )
