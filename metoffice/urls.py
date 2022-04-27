from django.urls import path

from .views import ForecastDataListAPIView


urlpatterns = [
    path('forecastdata/', ForecastDataListAPIView.as_view(), name='forecastdata-list')
]

