from django.urls import include, path

from .views import pdf_views

urlpatterns = [
    path("pdf-to-text", pdf_views.ExtractPDFTextView.as_view()),
    path("text-to-pdf", pdf_views.TextToPDFView.as_view()),
]
