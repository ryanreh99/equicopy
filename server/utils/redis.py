import redis


class Redis:
    def __init__(self) -> None:
        self.rclient = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            charset="utf-8",
            decode_responses=True,
        )


    def get_all_hashnames(self):
        return self.rclient.zrange("order", 0, -1)

    def get_column_names(self):
        hashnames = self.get_all_hashnames()
        if len(hashnames) == 0:
            return []
        return self.rclient.hkeys(hashnames[0])
    
    def get_all_hash_items(self, hashname):
        return self.rclient.hgetall(hashname)
    
    def flushall(self):
        return self.rclient.flushall()
    
    def get_pipeline(self):
        return self.rclient.pipeline()
    
    def is_empty(self):
        hashnames = self.get_all_hashnames()
        return len(hashnames) == 0

redis_api = Redis()