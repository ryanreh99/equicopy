import os

from django.shortcuts import render
from django.http import HttpResponse

from server.utils.redis import redis_api
from server.utils.response import json_success


def clean_column_name(name: str) -> str:
    return name.replace("_", " ").capitalize()


def fetch_data(request):
    if redis_api.is_empty():
        os.system("python manage.py fetch_copy")

    hashnames = redis_api.get_all_hashnames()
    column_names = redis_api.get_column_names()
    
    columns = [
        {
            "label": clean_column_name(column),
            "field": column,
        }
        for column in column_names
    ]
    rows = [
        redis_api.get_all_hash_items(hashname)
        for hashname in hashnames
    ]

    data = {
        "columns": columns,
        "rows": rows,
    }

    return json_success(data)
