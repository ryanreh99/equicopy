import json

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


def create_row_data(row) -> dict:
    return {
        'SC_CODE': row.__dict__['id'][6:],  # Remove "stock:" prefix
        **row.__dict__
    }


@check_redis
def get_csv_data(request: HttpRequest) -> HttpResponse:   
    url = get_url(redis_api.get_date())
    return HttpResponseRedirect(url)


@check_redis
def fetch_data(request: HttpRequest) -> HttpResponse:
    start = int(request.GET.get('start', 0))
    query_string = request.GET.get('query_string', '*')
    filters = request.GET.get('filters', {})

    if isinstance(filters, str):
        json_acceptable_string = filters.replace("'", "\"")
        filters = json.loads(json_acceptable_string)

    intervals = 100
    hashnames = redis_api.perform_search(query_string, start, start + intervals, filters)
    column_names = redis_api.get_column_names()
    
    columns = [
        create_column_data("SC_CODE")
    ] + [
        create_column_data(column)
        for column in column_names
    ]
    rows = [
        create_row_data(hashname)
        for hashname in hashnames
    ]

    data = {
        "columns": columns,
        "rows": rows,
    }

    return json_success(data)
