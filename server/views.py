from django.shortcuts import render
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect
)

from server.utils.fetch import get_url
from server.utils.redis import redis_api
from server.utils.response import json_success
from server.utils.decorators import check_redis


def create_column_data(column) -> dict:
    def clean_column_name(name: str) -> str:
        return name.replace("_", " ").capitalize()

    return {
            "label": clean_column_name(column),
            "field": column,
            "sort": True
        }


@check_redis
def get_csv_data(request: HttpRequest) -> HttpResponse:   
    url = get_url(redis_api.get_date())
    return HttpResponseRedirect(url)


@check_redis
def fetch_data(request: HttpRequest) -> HttpResponse:
    start = int(request.GET.get('start', 0))
    intervals = 100
    hashnames = redis_api.get_all_hashnames(start, start + intervals)
    column_names = redis_api.get_column_names()
    
    columns = [
        create_column_data("SC_CODE")
    ] + [
        create_column_data(column)
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
