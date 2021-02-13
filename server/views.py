import json
import redis

from django.shortcuts import render
from django.http import HttpResponse


def clean_column_name(name: str) -> str:
    return name.replace("_", " ").capitalize()


def fetch_data(request):
    rclient = redis.Redis(
                host='localhost',
                port=6379,
                db=0,
                charset="utf-8",
                decode_responses=True,
            )
    hashnames = rclient.zrange("order", 0, -1)
    column_names = rclient.hkeys(hashnames[0])
    
    columns = [
        {
            "label": clean_column_name(column),
            "field": column,
        }
        for column in column_names
    ]
    rows = [
        rclient.hgetall(hashname)
        for hashname in hashnames
    ]

    data = {
        "columns": columns,
        "rows": rows,
    }

    response = HttpResponse(
        content=json.dumps(
            data,
        ),
        content_type='application/json',
        status=200,
    )
    return response
