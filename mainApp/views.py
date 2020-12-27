from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core import serializers
from .forms import *
from .user_data import UserData
from .models import *
import json 

# Create your views here.

class UploadFile(LoginRequiredMixin, View):

    def post(self, request, pk):
        form = NewSeasonForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            season = Season(
                game_save = Save.objects.get(pk=pk),
                end_year = data['season_end_year'],
                division = data['division'],
                position = data['position'],
                teams_in_league = data['teams_in_league'],
                notes = data['notes']
            )
            season.save()
            user_data = UserData(request.FILES['file'], Save.objects.get(pk=pk), season, None)
            user_data._main()
            return redirect('save-page', pk=pk)
        else:
            return redirect('home')
    def get(self, request, pk):
        return render(request, 'mainApp/upload.html', {'pk':pk, 'form': NewSeasonForm()})


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
        
        players = Player.objects.filter(game_save=save)
        players_json = serializers.serialize('json', players)
        season_data = []
        seasons = save.season_set.all()
        
        for season in seasons:
            season_data.append({
                'year' : season.end_year,
                'division' : season.division,
                'position' : season.position,
                'teams_in_league' : season.teams_in_league
            })
        
        season_json = json.dumps(season_data)
        
        

        return render(request, 'mainApp/view_save.html', {'save': save, 'players_json': players_json, 'season_json':season_json})
    
