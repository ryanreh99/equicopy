from django.urls import path, re_path
from django.views.generic.base import RedirectView


from server.views import fetch_data

urlpatterns = [
    path('bhavcopy/', fetch_data, name='fetch-data'),
    re_path("^((?!static).)*$", RedirectView.as_view(url='static/index.html', permanent=False), name='index'),
]
