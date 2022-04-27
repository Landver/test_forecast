from django.urls import path
from metoffice.views import ForecastDataListAPIView


urlpatterns = [
    path('forecastdata/', ForecastDataListAPIView.as_view(), name='forecastdata-list')
]
