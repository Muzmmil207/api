from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


class EditorForm(forms.Form):
    content = forms.CharField(widget=CKEditorWidget())

def editor(request):

    form = EditorForm()
    context = {'form': form}
    return render(request, 'editor.html', context)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("adawatseo/", include("apps.adawatseo.urls")),
    path('',editor),
]
