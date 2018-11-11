from upload.models import BankStatement
import django_tables2 as tables
# Create your models here.


class BankStatementTable(tables.Table):

    class Meta:
        model = BankStatement
        fields = ('owner','bank_name', 'date', 'description','amount',
                  'category')
        # template_name = 'analysis/bs_table.html'