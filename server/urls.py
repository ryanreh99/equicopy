from django.urls import path

from server.views import fetch_data

urlpatterns = [
    path('bhavcopy/', fetch_data, name='fetch-data'),
]
