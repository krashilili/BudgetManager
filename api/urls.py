from django.urls import path, include
from api.views import BankStatementListView, BankStatementDetailView


urlpatterns = [
    path('bs/', BankStatementListView.as_view(), name='bankstatements'),
    path('bs/<int:pk>/', BankStatementDetailView.as_view(), name='bankstatements-detail' ),
]
