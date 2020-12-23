from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import *
from .user_data import UserData
from .models import *

# Create your views here.

class UploadFile(LoginRequiredMixin, View):

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print('hi')
            x = request.FILES['file']
            return UserData.parseHtml(x)
    def get(self, request):
        return render(request, 'mainApp/upload.html', {'form': UploadFileForm()})


class ViewSaves(LoginRequiredMixin, View):
    
    def get(self, request):
        saves = Save.objects.filter(user = request.user)
        return render(request, 'mainApp/saves.html', {'saves': saves})

class CreateSave(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'mainApp/create_save.html', {'form': CreateSaveForm()})
    
    def post(self, request):
        pass
        

        