from rest_framework import serializers
from upload import models


class BankStatementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.BankStatement
        fields = '__all__'
        lookup_field = 'date'