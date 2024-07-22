from django.urls import include, path

from .views import frontend_views, images_views, passwords_views, pdf_views

urlpatterns = [
    # PDF
    path("pdf-to-text", pdf_views.ExtractPDFTextView.as_view()),
    path("text-to-pdf", pdf_views.TextToPDFView.as_view()),
    # Frontend
    path("html-minifier", frontend_views.HTMLMinifierView.as_view()),
    path("html-beautifier", frontend_views.HTMLBeautifierView.as_view()),
    path("css-beautifier", frontend_views.CSSBeautifierView.as_view()),
    path("css-minifier", frontend_views.CSSMinifierView.as_view()),
    path("javascript-minifier", frontend_views.JavaScriptMinifierView.as_view()),
    path("javascript-beautifier", frontend_views.JavaScriptBeautifierView.as_view()),
    path("json-formatter", frontend_views.JSONFormatterView.as_view()),
    path("json-validator", frontend_views.JSONValidatorView.as_view()),
    path("json-minify", frontend_views.JSONMinifierView.as_view()),
    path("xml-to-json", frontend_views.XMLToJSONView.as_view()),
    path("json-to-xml", frontend_views.JSONToXMLView.as_view()),
    path("json-to-text", frontend_views.JSONToTextView.as_view()),
    path("csv-to-json", frontend_views.CSVToJSONView.as_view()),
    path("json-to-csv", frontend_views.JSONToCSVView.as_view()),
    path("tsv-to-json", frontend_views.TSVToJSONView.as_view()),
    # Images
    # path("image-converter",images_views.IcoToPngConverter.as_view()),
    # path("ico-converter", images_views.IcoToPngConverter.as_view()),
    # path("image-flipper",images_views.IcoToPngConverter.as_view()),
    # path("rotate-image",images_views.IcoToPngConverter.as_view()),
    # path("image-enlarger",images_views.IcoToPngConverter.as_view()),
    # path("image-cropper",images_views.IcoToPngConverter.as_view()),
    # path("image-resizer",images_views.IcoToPngConverter.as_view()),
    path("ico-to-png", images_views.IcoToPngConverter.as_view()),
    # path("jpg-converter",images_views.IcoToPngConverter.as_view()),
    path("webp-to-jpg", images_views.WebPToJpgConverter.as_view()),
    # path("png-to-webp",images_views.IcoToPngConverter.as_view()),
    # path("png-to-bmp",images_views.IcoToPngConverter.as_view()),
    # path("png-to-gif",images_views.IcoToPngConverter.as_view()),
    # path("png-to-ico",images_views.IcoToPngConverter.as_view()),
    # path("jpg-to-webp",images_views.IcoToPngConverter.as_view()),
    # path("jpg-to-bmp",images_views.IcoToPngConverter.as_view()),
    # path("jpg-to-gif",images_views.IcoToPngConverter.as_view()),
    # path("jpg-to-ico",images_views.IcoToPngConverter.as_view()),
    # path("webp-to-png",images_views.IcoToPngConverter.as_view()),
    # Password
    path("password-strength-checker", passwords_views.PasswordValidator.as_view()),
    path("password-encryption", passwords_views.PasswordEncryptionView.as_view()),
]
