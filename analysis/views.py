from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import RequestConfig
from upload.models import BankStatement
from .tables import BankStatementTable
# Create your views here.


class BankStatementListView(ListView):
    model = BankStatement
    template_name = 'analysis/bs_table.html'
    context_object_name = 'bankstatements'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BankStatementListView, self).get_context_data(**kwargs)
        table = BankStatementTable(BankStatement.objects.all())
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['table'] = table
        return context