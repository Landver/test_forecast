from mongoengine import Document, StringField, IntField


class ForecastData(Document):
    'Store values from www.metoffice.gov.uk'
    value = IntField()
    year = IntField()
    month = StringField()
    region = StringField()
    parameter = StringField()

    meta = {"indexes": ["region", "parameter"], "strict": False}
