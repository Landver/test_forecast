import re

from django.core.exceptions import FieldError, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ParseError

from .serializers import ForecastDataSerializer
from .models import ForecastData


class ForecastDataListAPIView(ListAPIView):
    queryset = ForecastData.objects.all()
    serializer_class = ForecastDataSerializer
    filter_fields = ["value", "year", "month", "region", "parameter"]

    def serialize_get_request(self, request):
        get_request = dict(request.GET)  # <QueryDict: {'a': ['1'], 'c': ['3']}> become {'a': ['1'], 'c': ['3']}

        for key, value in get_request.items():
            if len(value) == 1:              # all values that has only 1 object in list, like {'a': ['1'], 'c': ['3']}
                get_request[key] = value[0]  # become regular value, like {'a': '1', 'c': '3'}

        return get_request

    def get_kwargs_for_queryset_filtering(self):
        kwargs = {}
        serialized_get_request = self.serialize_get_request(self.request)

        for key, value in serialized_get_request.items():
            # requests always looks like: /?name__exact=Fortinet&date_time__gte='2006-01-01'&company=1
            # that's why we need to cut part "__exact" or anything like that
            if key.split('__')[0] not in self.filter_fields:
                continue

            # in case when user send : /?sitestatus=1&sitestatus=2, we actually get sitestatus=["1","2"],
            # and of course we can't do filter by that key/value pair, we need to make sitestatus__in=["1","2"],
            # exception will be if we have create_date__range=["2018", "2019"] or site__name__in=["Active", "Suspended"]
            # Beware, here may be bugs!
            if type(value) is list:
                if not (re.search("__range$", key) or re.search("__in$", key)):
                    key += "__in"
            kwargs[key] = value

        return kwargs

    def filter_queryset(self, queryset):
        """original method. Heavily modified to use different filter lookup types of requests."""
        kwargs = self.get_kwargs_for_queryset_filtering()

        try:
            return queryset.filter(**kwargs)
        except (FieldError, ValidationError) as error:
            # FieldError may appear, for example, when user send "name__blabla=test" instead of "name__exact=test",
            # of course there is no lookup type "blabla" and database can't work with that query request.
            # ValidationError appear if user send wrong data in date/time, UUID types of fields
            self.request.user.search_filters.pop(self.table_or_form_name, None)
            self.request.user.save(update_fields=['search_filters'])
            detail = {"search request was broken": "you used search parameters, that can't be applied to database",
                      "the error text": str(error)}
            raise ParseError(detail=detail, code=400)
