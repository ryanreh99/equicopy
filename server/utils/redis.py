import redis


class Redis:
    def __init__(self) -> None:
        self.hostname = 'localhost'
        self.port = 6379
        self.password = None
        self.db_number = 0

        self.rclient = redis.Redis(
            host=self.hostname,
            port=self.port,
            password=self.password,
            db=self.db_number,
            charset="utf-8",
            decode_responses=True,
        )


    def get_broker_url(self):
        broker_url = f'{self.hostname}:{self.port}/{self.db_number}'
        if self.password is not None:
            broker_url = f':{self.password}@{broker_url}'
        return "redis://" + broker_url

    def get_all_hashnames(self, start=0, end=-1):
        return self.rclient.zrange("order", start, end)

    def get_column_names(self):
        hashnames = self.get_all_hashnames(0, 1)
        if len(hashnames) == 0:
            return []
        return self.rclient.hkeys(hashnames[0])
    
    def get_all_hash_items(self, hashname):
        ret = self.rclient.hgetall(hashname)
        ret["SC_CODE"] = hashname
        return ret
    
    def get_date(self):
        return self.rclient.get("date")
    
    def flushall(self):
        return self.rclient.flushall()
    
    def get_pipeline(self):
        return self.rclient.pipeline()
    
    def is_empty(self):
        hashnames = self.get_all_hashnames(0, 1)
        return len(hashnames) == 0

redis_api = Redis()