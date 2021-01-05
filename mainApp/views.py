from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core import serializers
from .forms import *
from .user_data import UserData, calculate_best_players
from .models import *
import json 
from django.contrib import messages
import collections

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
            state = user_data._main()
            if state == "FINE":
                return redirect('save-page', pk=pk)
            elif state == "HTML":
                messages.warning(request, "Oops - that wasn't an HTML file")
            elif state == "PANDAS":
                messages.warning(request, "Hmm, that HTML file was weird. Are you sure it has a table?")
            else:
                messages.warning(request, "Hmm, that HTML file was weird. Are you sure you're using the correct squad view?")
            return render(request, 'mainApp/upload.html', {'pk':pk, 'form': NewSeasonForm()})

        else:
            return redirect('home')
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return render('login')
        elif Save.objects.get(pk=pk).user != request.user:
            return render('view-saves')
        return render(request, 'mainApp/upload.html', {'pk':pk, 'form': NewSeasonForm()})


class ViewSaves(LoginRequiredMixin, View):
    
    def get(self, request):
        if not request.user.is_authenticated:
            return render('login')
        saves = Save.objects.filter(user = request.user)


        return render(request, 'mainApp/saves.html', {'saves': saves})

class CreateSave(LoginRequiredMixin, View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render('login')
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

    @staticmethod
    def calculate_rating_wage(save: Save) -> dict:
        seasons = save.season_set.all()
        labels = []
        ratings = []
        wages = []
        for s in seasons:
            pseasons = s.playerseason_set.all()
            for ps in pseasons:
                if ps.appearances >= 10:
                    labels.append(f'{ps.player.name}, {ps.season.end_year}')
                    ratings.append(ps.average_rating)
                    wages.append(ps.wage)
        return {'labels': labels, 'ratings': ratings, 'wages': wages}
    
    @staticmethod
    def calculate_season_positions(save: Save):
        seasons = save.season_set.all()
        divisions = {}
        print(seasons)
        for season in seasons:
            divisions.update({season.division : season.teams_in_league})
        total_teams = 0
        division_pos = {}
        tickvals = []
        ticktext = []
        for key in sorted(divisions, reverse=True):
            division_pos.update({key: total_teams})
            total_teams += divisions[key]
            tickvals.append(total_teams)
            ticktext.append(f'Div {key}')
        season_positions = {'seasons': [], 'ys': [], 'labels': [], 'ticktext': ticktext, 'tickvals': tickvals}
        num_to_word = {1: '1st', 2: '2nd', 3: '3rd'}
        for season in seasons:
            boost = division_pos[season.division]
            true_y = divisions[season.division] - season.position + boost
            if season.position <= 3:
                label = f'Div {season.division}, {num_to_word[season.position]} place'
            else:
                label = f'Div {season.division}, {season.position}th place'
            season_positions['seasons'].append(season.end_year)
            season_positions['ys'].append(true_y)
            season_positions['labels'].append(label)
        
        if len(season_positions['seasons']) < 10:
            season_positions['seasons'] = [i + season_positions['seasons'][0] for i in range (0,10)]
        else:
            season_positions['seasons'] = season_positions['seasons'][-10:]

        json_data = {'max': total_teams, 'pos': season_positions}
        return json_data

    def get(self, request, pk):
        save = Save.objects.get(pk=pk)
        if save.user != request.user:
            return redirect('view-saves')
        
        players = Player.objects.filter(game_save=save)
        players_json = serializers.serialize('json', players)
        season_data = []
        seasons = save.season_set.all()
        calculate_best_players(save)
        for season in seasons:
            season_data.append({
                'pk': season.pk,
                'year' : season.end_year,
                'division' : season.division,
                'position' : season.position,
                'teams_in_league' : season.teams_in_league
            })
        
        season_json = json.dumps(season_data)
        
        save_no = json.dumps(pk)
        
        season_positions = json.dumps(SaveView.calculate_season_positions(save))
        return render(request, 'mainApp/view_save.html', {'save': save, 'players_json': players_json, 'season_json':season_json, 'save_no': save_no, 'season_positions':season_positions})
    

class PlayerView(View):

    def post(self, request):
        pass

    @staticmethod
    def get_years_played(player: Player) -> str:
        '''
        If a player has played in 2020-2021, 2021-2022, 2022-23, 2024-25, 2025-26 seasons, then this will return "2020-2023, 2024-26"
        '''
        playing_years = list()
        for s in player.playerseason_set.all():
            playing_years.append(s.season.end_year)
        playing_years.sort()
        index = 0
        ovr_str = ""
        while index < len(playing_years):
            start_yr = playing_years[index]
            cur_str = f'{start_yr-1}-'
            cur_year = playing_years[index]
            while index + 1 < len(playing_years) and playing_years[index+1] <= cur_year + 1:
                cur_year = playing_years[index+1]
                index += 1
            if start_yr == cur_year:
                cur_str = cur_str[:-1]
            else:
                cur_str += str(cur_year)
            index += 1
            ovr_str += cur_str
            ovr_str += ", "
        return ovr_str[:-2]
    
    @staticmethod
    def get_indicator_95th():
        _player_count = Player.objects.all().count()
        _95thpercentile = int(0.05 * _player_count)
        data = {}
        data.update({'gls/90': Player.objects.order_by('-goals_per_90')[_95thpercentile].goals_per_90})
        data.update({'shots/90': Player.objects.order_by('-shots_per_90')[_95thpercentile].shots_per_90})
        data.update({'asts/90': Player.objects.order_by('-assists_per_90')[_95thpercentile].assists_per_90})
        data.update({'dribbles/90': Player.objects.order_by('-dribbles_per_90')[_95thpercentile].dribbles_per_90})
        data.update({'key_passes/90': Player.objects.order_by('-key_passes_per_90')[_95thpercentile].key_passes_per_90})
        data.update({'interceptions/90': Player.objects.order_by('-int_per_90')[_95thpercentile].int_per_90})
        data.update({'tackles/90': Player.objects.order_by('-tackles_per_90')[_95thpercentile].tackles_per_90})
        return json.dumps(data)


    def get(self, request, pk, name):
        save = Save.objects.get(pk=pk)
        if save.user != request.user:
            return render('view-saves')
        name = name.replace("_", " ")
        player = save.player_set.all().get(name=name)
        playerdata = {
            'gls/90': player.goals_per_90,
            'shots/90': player.shots_per_90,
            'asts/90': player.assists_per_90,
            'dribbles/90': player.dribbles_per_90,
            'key_passes/90': player.key_passes_per_90,
            'interceptions/90': player.int_per_90,
            'tackles/90': player.tackles_per_90
        }
        playerdata_json = json.dumps(playerdata)
        percentile_data = PlayerView.get_indicator_95th()
        playerseasons = serializers.serialize('json',player.playerseason_set.all())
        years_played = PlayerView.get_years_played(player)
        seasons = json.dumps(dict(Season.objects.values_list('pk', 'end_year')))
        return render(request, 'mainApp/view_player.html', {'player': player, 'playerdata_json': playerdata_json, 'playerseasons':playerseasons, 'playingyears':years_played, 'seasons': seasons, 'percentile_data': percentile_data})


class SeasonView(View):

    def get(self, request, pk, pk2):
        save = Save.objects.get(pk=pk)
        if save.user != request.user:
            return render('view-saves')
        season = Season.objects.get(pk=pk2)
        players = serializers.serialize('json', season.playerseason_set.all())
        return render(request, 'mainApp/view_season.html', {'season':season, 'players': players})

    def post(self, request):
        pass

class DeleteSave(View):

    def get(self, request, pk):
        save = Save.objects.get(pk=pk)
        if save.user != request.user:
            return render('view-saves')
        print(save.pk)
        return render(request, 'mainApp/delete_save.html', {'save': save})

    def post(self, request, pk):
        Save.objects.get(pk=pk).delete()
        messages.success(request, 'Save deleted')
        return redirect('view-saves')
