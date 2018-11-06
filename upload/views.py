from django.shortcuts import render, HttpResponse

from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from .forms import UploadBankStatementDocumentForm
from .models import BankStatementDocument, BankStatement
from tablib import Dataset
from .resources import BankStatementResource
from import_export import resources
import pandas as pd
from io import StringIO
from datetime import datetime as dt


def find_category_of_transaction(trans_des):
    obj = BankStatement.objects.filter(description=trans_des).first()
    try:
        if obj.category:
            return obj.category
    except:
        return None


def handle_bank_statement(f, resource_instance, doc_instance):

    # bank name
    bank_name =  doc_instance.bank.lower() if doc_instance.bank else None

    for chunk in f.chunks():
        s = str(chunk, 'utf-8')
        data = StringIO(s)
        if bank_name == 'discover':
            df = pd.read_csv(data)
            df.columns = ['date', 'post', 'description', 'amount', 'category']
            # df['id'] = None

        elif bank_name == 'american express':
            df = pd.read_csv(data, header=None, index_col=None)
            df = df.dropna(axis='columns')
            # Rename the columns
            df.rename(columns={df.columns[0]: 'date',
                               df.columns[1]: 'description',
                               df.columns[2]: 'amount'},
                      inplace=True)
            # Convert the date format to 'YYYY-MM-DD'
            df['date'] = df['date'].apply(lambda d: d.split(' ')[0])
            df = df.rename(columns={df.columns[0]: 'date', df.columns[1]: 'description', df.columns[2]: 'amount'})
            df['date'] = df['date'].apply(lambda d: dt.strptime(d, "%m/%d/%Y")).apply(
                lambda d: d.strftime('%Y-%m-%d'))

            df['category'] = df['description'].apply(lambda c: find_category_of_transaction(c))

        df['owner'] = doc_instance.owner
        df['bank_name'] = doc_instance.bank
        df['statement_source'] = doc_instance.slug
        df.to_csv('./media/temp/temp.csv')

        imported_data = Dataset().load(open('./media/temp/temp.csv').read())
        result = resource_instance.import_data(imported_data, dry_run=True)  # Test the data import

        if not result.has_errors():
            resource_instance.import_data(imported_data, dry_run=False)  # Actually import now


class BasicUploadView(View):
    form_class = UploadBankStatementDocumentForm
    template_name = 'upload/bankstatement_form.html'

    def get(self, request):
        form = self.form_class()

        return render(request,
                      self.template_name,
                      {'form':form})

    def post(self, request):
        # form = DocumentForm(request.POST, request.FILES)
        # bank_statement_resource = resources.modelresource_factory(model=BankStatement)()

        bound_form = self.form_class(request.POST, request.FILES)
        if bound_form.is_valid():
            doc_instance = bound_form.save()
            # instantiate bank statement
            bank_statement_resource = BankStatementResource()
            if bank_statement_resource:
                handle_bank_statement(request.FILES['file'], bank_statement_resource, doc_instance)
            return HttpResponse('statements upload success')
        else:
            return render(request=request,
                          template_name=self.template_name,
                          context={'form': bound_form})


def clear_database(request):
    for photo in BankStatementDocument.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))
