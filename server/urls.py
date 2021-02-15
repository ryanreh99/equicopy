from django.urls import path, re_path
from django.views.generic.base import RedirectView


from server.views import fetch_data, get_csv_data

urlpatterns = [
    path('bhavcopy/', fetch_data, name='fetch-data'),
    path('getCSV/', get_csv_data, name='get-csv-data'),
    re_path("^((?!static).)*$", RedirectView.as_view(url='static/index.html', permanent=False), name='index'),
]
