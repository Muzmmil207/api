from django.urls import include, path

from . import views

urlpatterns = [
    path("pdf-to-text", views.ExtractPDFTextView.as_view()),
    path("text-to-pdf", views.TextToPDFView.as_view()),
]
