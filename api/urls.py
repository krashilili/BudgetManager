from django.urls import path, include
from api.views import BankStatementListView, BankStatementDetailView


urlpatterns = [
    path('bs/', BankStatementListView.as_view(), name='api_bs'), # a list of all bank statements
    path('bs/<str:date>/', BankStatementDetailView.as_view(), name='api_bs_by_date' ),
    path('bs/<str:date>/<str:bank_name>/', BankStatementDetailView.as_view(), name='api_bs_by_date_and_bank'),
]
