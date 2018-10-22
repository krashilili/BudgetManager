from import_export import resources
from .models import BankStatement


class BankStatementResource(resources.ModelResource):
    class Meta:
        model = BankStatement
        # fields = ('id', 'date', 'post',
        #           'description',  'amount', 'category',)
        # exclude = ('post_date',)