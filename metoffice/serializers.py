
from rest_framework.serializers import (
    Serializer,
    CharField,
    IntegerField,
    FloatField
)


class ForecastDataSerializer(Serializer):
    value = FloatField()
    year = IntegerField()
    month = CharField()
    region = CharField()
    parameter = CharField()
