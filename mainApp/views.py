from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import *
from .user_data import UserData
from .models import *

# Create your views here.

class UploadFile(LoginRequiredMixin, View):

    def post(self, request, pk):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            UserData.parseHtml(request.FILES['file'])
            return redirect('view-saves')
        else:
            return redirect('home')
    def get(self, request, pk):
        return render(request, 'mainApp/upload.html', {'pk':pk, 'form': UploadFileForm()})


class ViewSaves(LoginRequiredMixin, View):
    
    def get(self, request):
        saves = Save.objects.filter(user = request.user)
        return render(request, 'mainApp/saves.html', {'saves': saves})

class CreateSave(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'mainApp/create_save.html', {'form': CreateSaveForm()})
    
    def post(self, request):
        form = CreateSaveForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            s = Save(
                user = request.user,
                team = data['team'],
                currency = "$",
                height_choice = data['height_choice'],
                wage_period = data['wage_period'],
                distance_choice = data['distance_choice']
            )
            s.save()
            return redirect('view-saves')
        
class SaveView(View):

    def post(self, request):
        pass

    def get(self, request, pk):
        save = Save.objects.get(pk=pk)
        if save.user != request.user:
            return redirect('view-saves')
        
        return render(request, 'mainApp/view_save.html', {'save': save})
    
