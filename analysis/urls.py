from django.urls import path
from .views import BankStatementListView
from django.conf.urls import url, include
from django.views.generic import TemplateView


urlpatterns = [
    path('table', BankStatementListView.as_view(), name='bs_table'),
    path('dashboard', TemplateView.as_view(template_name='analysis/dashboard.html'), name='dashboard'),
]