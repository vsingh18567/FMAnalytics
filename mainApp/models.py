from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.
class Save(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    team = models.CharField(max_length=150)
    date = models.DateField(auto_now_add=True)
    seasons = models.IntegerField(default=0)
    currency = models.CharField(max_length=5)
    height_choice = models.CharField(max_length=3)
    wage_period = models.CharField(max_length=5)
    distance_choice = models.CharField(max_length=5)

    def __str__(self):
        return str(self.pk) + '|' + str(self.user) + '|' + str(self.team)
    
class Season(models.Model):
    game_save = models.ForeignKey(Save, on_delete=CASCADE)
    end_year = models.IntegerField()
    division = models.IntegerField()
    position = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return str(self.pk) + '|' + str(self.game_save.user) + '|' + str(self.end_year)

class Player(models.Model):
    game_save = models.ForeignKey(Save, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=3)
    seasons = models.IntegerField()
    appearances = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    average_rating = models.FloatField()
    pom = models.IntegerField()
    reds = models.IntegerField()
    yellows = models.IntegerField()
    best_role = models.CharField(max_length=30)
    max_value = models.FloatField()
    home_grown_status = models.BooleanField()

    def __str__(self):
        return str(self.pk) + '|' + str(self.game_save.user) + '|' + str(self.name)

class PlayerSeason(models.Model):
    season = models.ForeignKey(Season, on_delete=CASCADE)
    player = models.ForeignKey(Player, on_delete=CASCADE)
    best_role = models.CharField(max_length=4)
    age = models.IntegerField()
    wage = models.IntegerField()
    playing_time = models.CharField(max_length=150)
    value = models.FloatField()
    determination = models.IntegerField()
    teamwork = models.IntegerField()
    leadership = models.IntegerField()
    appearances = models.IntegerField()
    minutes = models.IntegerField()
    average_rating = models.FloatField()
    pom = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    reds = models.IntegerField()
    yellows = models.IntegerField()
    clean_sheets = models.IntegerField()
    conceded = models.IntegerField()
    goal_mistakes = models.IntegerField()
    header_percent = models.IntegerField()
    int_per_90 = models.FloatField()
    tackles = models.FloatField()
    tackle_ratio = models.FloatField()
    cr_c = models.IntegerField()
    dist_per_90 = models.FloatField()
    dribbles = models.IntegerField()
    pass_completion = models.FloatField()
    key_passes = models.IntegerField()
    penalties = models.IntegerField()
    xG = models.FloatField()
    shots = models.IntegerField()
    shot_percent = models.IntegerField()

    def __str__(self):
        return str(self.pk) + '|' + str(self.player.game_save.user) + '|' + str(self.player.name)