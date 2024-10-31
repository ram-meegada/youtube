from django.urls import path
from . import views

urlpatterns = [
    path("provide-options/", views.FetchLinkAndGiveOptionsView.as_view()),
    path("download-file/", views.DownloadFileView.as_view()),

]
