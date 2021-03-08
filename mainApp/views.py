from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core import serializers
from .forms import *
from .user_data import *
from .models import *
import json
from django.contrib import messages
import collections
from .calculations import *


# Create your views here.


class UploadFile(LoginRequiredMixin, View):
    """
    url: 'upload'
    """

    def post(self, request, pk):
        form = NewSeasonForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            seasons = Save.objects.get(pk=pk).season_set.all()
            for s in seasons:
                if s.end_year == data["season_end_year"]:
                    messages.warning(
                        request,
                        "You already have a season with that end year in the database.",
                    )
                    return render(
                        request,
                        "mainApp/upload.html",
                        {"pk": pk, "form": NewSeasonForm()},
                    )
                elif data["teams_in_league"] < data["position"]:
                    messages.warning(
                        request,
                        "Your team can't finish lower than the number of teams in the league",
                    )
                    return render(
                        request,
                        "mainApp/upload.html",
                        {"pk": pk, "form": NewSeasonForm()},
                    )
            season = Season(
                game_save=Save.objects.get(pk=pk),
                end_year=data["season_end_year"],
                division=data["division"],
                position=data["position"],
                teams_in_league=data["teams_in_league"],
                notes=data["notes"],
            )
            user_data = UserData(
                request.FILES["file"], Save.objects.get(pk=pk), season, None
            )
            season.save()
            state = user_data._main()
            if state == "FINE":
                return redirect("save-page", pk=pk)
            elif state == "HTML":
                messages.warning(request, "Oops - that wasn't an HTML file")
            elif state == "PANDAS":
                messages.warning(
                    request,
                    "Hmm, that HTML file was weird. Are you sure it has a table?",
                )
            else:
                messages.warning(
                    request,
                    "Hmm, that HTML file was weird. Are you sure you're using the correct squad view?",
                )
            season.delete()
            return render(
                request, "mainApp/upload.html", {"pk": pk, "form": NewSeasonForm()}
            )
        else:
            return redirect("home")

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return render("login")
        elif Save.objects.get(pk=pk).user != request.user:
            return render("view-saves")
        return render(
            request, "mainApp/upload.html", {"pk": pk, "form": NewSeasonForm()}
        )


class ViewSaves(LoginRequiredMixin, View):
    """
    url: view-saves
    """

    def get(self, request):
        if not request.user.is_authenticated:
            return render("login")
        saves = Save.objects.filter(user=request.user).order_by("-date")

        return render(request, "mainApp/saves.html", {"saves": saves})


class CreateSave(LoginRequiredMixin, View):
    """
    url: create-save
    """

    def get(self, request):
        if not request.user.is_authenticated:
            return render("login")
        return render(request, "mainApp/create_save.html", {"form": CreateSaveForm()})

    def post(self, request):
        form = CreateSaveForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            s = Save(
                user=request.user,
                team=data["team"],
            )
            s.save()
            return redirect("view-saves")


class SaveView(LoginRequiredMixin, View):
    """
    url: save-page
    """

    def post(self, request):
        pass

    @staticmethod
    def calculate_rating_wage(save: Save) -> dict:
        """
        unused method - used to generate rating/wage scatter
        chart
        """
        seasons = save.season_set.all()
        labels = []
        ratings = []
        wages = []
        for s in seasons:
            pseasons = s.playerseason_set.all()
            for ps in pseasons:
                if ps.appearances >= 10:
                    labels.append(f"{ps.player.name}, {ps.season.end_year}")
                    ratings.append(ps.average_rating)
                    wages.append(ps.wage)
        return {"labels": labels, "ratings": ratings, "wages": wages}

    def get(self, request, pk):
        save = Save.objects.get(pk=pk)
        if save.user != request.user:
            return redirect("view-saves")

        players = Player.objects.filter(game_save=save)
        players_json = serializers.serialize("json", players)
        season_data = []
        seasons = save.season_set.all()
        for season in seasons:
            season_data.append(
                {
                    "pk": season.pk,
                    "year": season.end_year,
                    "division": season.division,
                    "position": season.position,
                    "teams_in_league": season.teams_in_league,
                }
            )

        season_json = json.dumps(season_data)

        save_no = json.dumps(pk)
        # best defenders, creators, attackers
        best_players = calculate_best_players2(save.player_set.all(), "name")
        # data for the seasons chart
        season_positions = json.dumps(calculate_season_positions(save))
        return render(
            request,
            "mainApp/view_save.html",
            {
                "save": save,
                "players_json": players_json,
                "season_json": season_json,
                "save_no": save_no,
                "season_positions": season_positions,
                "best_players": json.dumps(best_players),
            },
        )


class PlayerView(LoginRequiredMixin, View):
    """
    url: player-page
    """

    def post(self, request):
        pass

    @staticmethod
    def get_indicator_95th():
        """
        get the 95th percentile for the radar chart on the player
        page
        """
        _player_count = Player.objects.all().count()
        _95thpercentile = int(0.05 * _player_count)
        data = {}
        data.update(
            {
                "gls/90": Player.objects.order_by("-goals_per_90")[
                    _95thpercentile
                ].goals_per_90
            }
        )
        data.update(
            {
                "shots/90": Player.objects.order_by("-shots_per_90")[
                    _95thpercentile
                ].shots_per_90
            }
        )
        data.update(
            {
                "asts/90": Player.objects.order_by("-assists_per_90")[
                    _95thpercentile
                ].assists_per_90
            }
        )
        data.update(
            {
                "dribbles/90": Player.objects.order_by("-dribbles_per_90")[
                    _95thpercentile
                ].dribbles_per_90
            }
        )
        data.update(
            {
                "key_passes/90": Player.objects.order_by("-key_passes_per_90")[
                    _95thpercentile
                ].key_passes_per_90
            }
        )
        data.update(
            {
                "interceptions/90": Player.objects.order_by("-int_per_90")[
                    _95thpercentile
                ].int_per_90
            }
        )
        data.update(
            {
                "tackles/90": Player.objects.order_by("-tackles_per_90")[
                    _95thpercentile
                ].tackles_per_90
            }
        )
        return json.dumps(data)

    def get(self, request, pk, name):
        save = Save.objects.get(pk=pk)
        if save.user != request.user:
            return render("view-saves")
        name = name.replace("_", " ")
        player = save.player_set.all().get(name=name)
        playerdata = {
            "gls/90": player.goals_per_90,
            "shots/90": player.shots_per_90,
            "asts/90": player.assists_per_90,
            "dribbles/90": player.dribbles_per_90,
            "key_passes/90": player.key_passes_per_90,
            "interceptions/90": player.int_per_90,
            "tackles/90": player.tackles_per_90,
        }
        playerdata_json = json.dumps(playerdata)
        percentile_data = PlayerView.get_indicator_95th()
        playerseasons = serializers.serialize("json", player.playerseason_set.all())
        years_played = get_years_played(player)
        seasons = json.dumps(dict(Season.objects.values_list("pk", "end_year")))
        return render(
            request,
            "mainApp/view_player.html",
            {
                "player": player,
                "playerdata_json": playerdata_json,
                "playerseasons": playerseasons,
                "playingyears": years_played,
                "seasons": seasons,
                "percentile_data": percentile_data,
            },
        )


class SeasonView(LoginRequiredMixin, View):
    """
    url: season-page
    """

    def get(self, request, pk, pk2):
        save = Save.objects.get(pk=pk)
        if save.user != request.user:
            return render("view-saves")
        season = Season.objects.get(pk=pk2)
        players = json.dumps(dict(Player.objects.values_list("pk", "name")))
        best_players = json.dumps(
            calculate_best_players(season.playerseason_set.all(), "player_id")
        )
        playerseasons = serializers.serialize("json", season.playerseason_set.all())
        return render(
            request,
            "mainApp/view_season.html",
            {
                "season": season,
                "players": players,
                "playerseasons": playerseasons,
                "best_players": best_players,
            },
        )

    def post(self, request):
        pass


class DeleteSave(LoginRequiredMixin, View):
    """
    url: delete-save
    """

    def get(self, request, pk):
        save = Save.objects.get(pk=pk)
        if save.user != request.user:
            return render("view-saves")
        print(save.pk)
        return render(request, "mainApp/delete_save.html", {"save": save})

    def post(self, request, pk):
        Save.objects.get(pk=pk).delete()
        messages.success(request, "Save deleted")
        return redirect("view-saves")


class DeleteSeason(LoginRequiredMixin, View):
    def get(self, request, pk, pk2):
        season = Season.objects.get(pk=pk2)
        if season.game_save.user != request.user:
            return render("view-saves")
        return render(request, "mainApp/delete_season.html", {"season": season})

    def post(self, request, pk, pk2):
        season = Season.objects.get(pk=pk2)
        season.game_save.seasons -= 1
        season.game_save.save()
        delete_season(season)
        season.delete()
        messages.success(request, "Season deleted")
        return redirect("save-page", pk)


class EditSeason(LoginRequiredMixin, View):
    def get(self, request, pk, pk2):
        season = Season.objects.get(pk=pk2)
        return render(
            request,
            "mainApp/edit_season.html",
            {
                "season": season,
                "form": EditSeasonForm(
                    initial={
                        "season_end_year": season.end_year,
                        "division": season.division,
                        "position": season.position,
                        "teams_in_league": season.teams_in_league,
                        "notes": season.notes,
                    }
                ),
            },
        )

    def post(self, request, pk, pk2):
        form = EditSeasonForm(request.POST)
        season = Season.objects.get(pk=pk2)
        if form.is_valid():
            data = form.cleaned_data
            seasons = Save.objects.get(pk=pk).season_set.all()
            for s in seasons:
                if s.end_year == data["season_end_year"] and s.pk != pk2:
                    messages.warning(
                        request,
                        "You already have a season with that end year in the database.",
                    )
                    return redirect("edit-season", pk, pk2)
                elif data["teams_in_league"] < data["position"]:
                    messages.warning(
                        request,
                        "Your team can't finish lower than the number of teams in the league",
                    )
                    return redirect("edit-season", pk, pk2)
            season.end_year = data["season_end_year"]
            season.division = data["division"]
            season.position = data["position"]
            season.teams_in_league = data["teams_in_league"]
            season.notes = data["notes"]
            season.save()
            messages.success(request, "Season edited successfully")
            return redirect("season-page", pk, pk2)
        return render(
            request,
            "mainApp/edit_season.html",
            {
                "season": season,
                "form": EditSeasonForm(
                    initial={
                        "season_end_year": season.end_year,
                        "division": season.division,
                        "position": season.position,
                        "teams_in_league": season.teams_in_league,
                        "notes": season.notes,
                    }
                ),
            },
        )
