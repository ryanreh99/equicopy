
import os

from server.utils.redis import redis_api


def check_redis(function):
    def wrap(request, *args, **kwargs):
        if redis_api.is_empty():
            os.system("python manage.py fetch_copy")
        return function(request, *args, **kwargs)


    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap