import redis
from redisearch import (
    Query,
    Client,
    TextField,
    NumericField,
    NumericFilter,
    IndexDefinition,
)


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

        self.numeric_indexes = [
            'OPEN',
            'HIGH',
            'LOW',
            'CLOSE',
            'LAST',
            'PREVCLOSE',
            'NO_TRADES',
            'NO_OF_SHRS',
            'NET_TURNOV',
        ]


    def get_broker_url(self):
        broker_url = f'{self.hostname}:{self.port}/{self.db_number}'
        if self.password is not None:
            broker_url = f':{self.password}@{broker_url}'
        return "redis://" + broker_url

    def get_indexed_client(self):
        return Client(
            "idx:stock",
            host=self.hostname,
            port=self.port,
            password=self.password,
        )
    
    def create_index(self):
        client = self.get_indexed_client()

        definition = IndexDefinition(prefix=['stock:'])

        index_fields = [TextField("SC_NAME"),]
        for index in self.numeric_indexes:
            index_fields.append(NumericField(index))

        try:
            # FT.CREATE idx:stock ON HASH PREFIX 1 stock: SCHEMA SC_NAME TEXT ...
            client.create_index(index_fields, definition=definition)
        except redis.exceptions.ResponseError as e:
            # FT.DROPINDEX idx:stock DD
            if (str(e) != "Index already exists"):
                raise e
    
    def get_query(self, query_string, limit_range, filters):
        INF = '+inf'
        NEG_INF = '-inf'
  
        q = Query(query_string)
        
        for index in self.numeric_indexes:
            lower, upper = NEG_INF, INF
            if filters.get(index) is not None:
                lower, upper = filters[index].split(',')
            q.add_filter(NumericFilter(index, lower, upper))

        q.limit_ids(*limit_range).paging(0, 4000)
        # default paging is performed for only 10 entries
        # We allow returning all entries (4000) and
        # paging is performed through the limit ids.

        return q

    def perform_search(self, query_string, start=0, end=-1, filters={}):
        # We are paginating with `limit_range` and thus
        # don't want it to be empty, as then it is the
        # default case and returns all results instead of None.
        limit_range = self.get_all_hashnames(start, end)
        limit_range.append(-1)

        client = self.get_indexed_client()
        q = self.get_query(query_string, limit_range, filters)
        return client.search(q).docs

    def get_all_hashnames(self, start=0, end=-1):
        return self.rclient.zrange("order", start, end)

    def get_column_names(self):
        hashnames = self.get_all_hashnames(0, 1)
        if len(hashnames) == 0:
            return []
        return self.rclient.hkeys(hashnames[0])
    
    def get_all_hash_items(self, hashname):
        ret = self.rclient.hgetall(hashname)
        ret["SC_CODE"] = hashname[6:] # Remove "stock:" prefix
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