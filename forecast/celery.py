from os import environ as env

from celery import Celery
from celery.schedules import crontab


env.setdefault('DJANGO_SETTINGS_MODULE', 'forecast.settings')

app = Celery('forecast')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    sender.add_periodic_task(crontab(day_of_month=1), parse_metoffice.s())

@app.task
def parse_metoffice():
    from requests import request
    import pandas as pd


    regions = [
        'UK',
        'England',
        'Wales',
        'Scotland',
        'Northern_Ireland',
        'England_and_Wales',
        'England_N',
        'England_S',
        'Scotland_N',
        'Scotland_E',
        'Scotland_W',
        'England_E_and_NE',
        'England_NW_and_N_Wales',
        'Midlands',
        'East_Anglia',
        'England_SW_and_S_Wales',
        'England_SE_and_Central_S'
    ]

    parameters = [
        'AirFrost',
        'Raindays1mm',
        'Rainfall',
        'Sunshine',
        'Tmean',
        'Tmin',
        'Tmax'
    ]

    for region in regions:
        for parameter in parameters:
            url = f'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter}/date/{region}.txt'
            response = request(url=url, method='GET')
            content = response.content.decode('utf-8')
