from mongoengine import Document, StringField, FloatField, IntField


class ForecastData(Document):
    'Store values from www.metoffice.gov.uk'
    value = FloatField()
    year = IntField()
    month = StringField()
    region = StringField()
    parameter = StringField()

    meta = {"indexes": ["region", "parameter"], "strict": False}
