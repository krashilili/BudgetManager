from django import forms

from .models import BankStatementDocument


class UploadBankStatementDocumentForm(forms.ModelForm):

    class Meta:
        model = BankStatementDocument
        fields = ['owner','bank','file']

    # def clean_slug(self):
    #     """
    #     Lowercase the slug
    #     :return:
    #     """
    #     return self.cleaned_data['slug'].lower()