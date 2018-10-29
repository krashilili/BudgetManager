from django.shortcuts import render
from django.utils.dateparse import parse_date
from .serializers import BankStatementSerializer
from django.shortcuts import get_object_or_404
from upload.models import BankStatement
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import status



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
    GET bs/:id/
    PUT songs/:id/
    DELETE songs/:id/
    """
    #
    serializer_class = BankStatementSerializer
    queryset = BankStatement.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(BankStatementSerializer(a_song).data)
        except BankStatement.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
    #
    # def get_object(self):
    #     """
    #     This view should return a list of all the bankstatements
    #     on the date portion of the URL.
    #     :return:
    #     """
    #     #
    #     date = self.request.query_params.get('date')
    #     queryset = self.filter_queryset(self.get_queryset())
    #     obj = queryset.get(pk=self.request.)
    #     return queryset
    #
    #     # try:
    #     #     bankstatement = queryset.get(id=self.kwargs['id'])
    #     #     # return bankstatement
    #     #     return Response(BankStatementSerializer(bankstatement).data)
    #     # except BankStatement.DoesNotExist:
    #     #     return Response(
    #     #         data={
    #     #             "message": "BankStatement with id: {} does not exist".format(self.kwargs["id"])
    #     #         },
    #     #         status=status.HTTP_404_NOT_FOUND
    #     #     )
