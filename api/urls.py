from django.urls import path
from .views import RetrieveBankStatementListView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = {
    path('bslist/', RetrieveBankStatementListView.as_view({'get': 'list'}), name='details')
}

# urlpatterns = format_suffix_patterns(urlpatterns)
