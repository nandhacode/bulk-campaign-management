from django.shortcuts import render
from .forms import RecipientUploadForm

def call_form(request,message):
    form = RecipientUploadForm()
    return render(request, 'upload_file.html', {'form': form,'message':message})  