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


def handle_bank_statement(f, resource_instance, doc_instance):

    for chunk in f.chunks():
        s = str(chunk, 'utf-8')
        data = StringIO(s)
        df = pd.read_csv(data)
        df.columns = ['date', 'post', 'description', 'amount', 'category']
        df['id'] = None
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
