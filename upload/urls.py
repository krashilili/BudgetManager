from django.urls import path
from .views import BasicUploadView, clear_database
from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [

    path('clear/', clear_database, name='clear_database'),
    path('upload/', BasicUploadView.as_view(), name='basic_upload')
    # url(r'^progress-bar-upload/$', ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    # url(r'^drag-and-drop-upload/$', DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),

]