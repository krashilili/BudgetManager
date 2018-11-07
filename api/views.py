from django.shortcuts import render
from django.utils.dateparse import parse_date
from .serializers import BankStatementSerializer
from django.shortcuts import get_object_or_404
from upload.models import BankStatement
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import status
import datetime as dt



class MultipleFieldLookupORMixin(object):
    """
    Actual code http://www.django-rest-framework.org/api-guide/generic-views/#creating-custom-mixins
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            try:  # Get the result with one or more fields.
                filter[field] = self.kwargs[field]
            except Exception:
                pass
        return get_object_or_404(queryset, **filter)  # Lookup the object


# Create your views here.
class BankStatementListView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = BankStatement.objects.all()
    serializer_class = BankStatementSerializer
    # lookup_field = 'date'


class BankStatementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET bs/:date/
    PUT bs/:date/
    DELETE bs/:date/
    """
    #
    serializer_class = BankStatementSerializer
    queryset = BankStatement.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            # query the bank statements by transaction date
            # qet the bank name
            bank = kwargs.get('bank_name')
            date = kwargs.get('date')
            bs = None
            if date:
                if date.lower() == 'all' and bank:
                    bs = BankStatement.objects.filter(bank_name=bank)
                elif date.lower() == 'all'and not bank:
                    bs = BankStatement.objects.filter()
                elif bank:
                    trans_date = dt.datetime.strptime(date,'%Y-%m-%d')
                    bs = BankStatement.objects.filter(date=trans_date, bank_name=bank)
                elif not bank:
                    trans_date = dt.datetime.strptime(date, '%Y-%m-%d')
                    bs = BankStatement.objects.filter(date=trans_date)
            else:
                bs = BankStatement.objects.filter()

            return Response(BankStatementSerializer(bs, many=True).data)
        except BankStatement.DoesNotExist:
            return Response(
                data={
                    "message": "Bankstatement with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

