from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


# Create your models here.
class Save(models.Model):
	user = models.ForeignKey(User, on_delete=CASCADE)
	team = models.CharField(max_length=150)
	date = models.DateField(auto_now_add=True)
	seasons = models.IntegerField(default=0)

	def __str__(self):
		return str(self.pk) + '|' + str(self.user) + '|' + str(self.team)


class Season(models.Model):
	game_save = models.ForeignKey(Save, on_delete=CASCADE)
	end_year = models.IntegerField()
	division = models.IntegerField()
	position = models.IntegerField()
	teams_in_league = models.IntegerField(default=20)
	notes = models.TextField(null=True, blank=True)

	def __str__(self):
		return str(self.pk) + '|' + str(self.game_save.user) + '|' + str(self.end_year)


class Player(models.Model):
	game_save = models.ForeignKey(Save, on_delete=CASCADE)
	name = models.CharField(max_length=100)
	nationality = models.CharField(max_length=3)
	seasons = models.IntegerField(default=0)
	appearances = models.IntegerField(default=0)
	minutes = models.IntegerField(default=0)
	minutes_per_season = models.FloatField(default=0)
	determination = models.IntegerField(default=0)
	teamwork = models.IntegerField(default=0)
	leadership = models.IntegerField(default=0)
	header_percent = models.IntegerField(default=0)
	goals = models.IntegerField(default=0)
	goals_per_90 = models.FloatField(default=0)
	xG = models.FloatField(default=0)
	goals_per_xG = models.FloatField(default=0)
	assists = models.IntegerField(default=0)
	assists_per_90 = models.FloatField(default=0)
	average_rating = models.FloatField(default=0)
	tackles_per_90 = models.FloatField(default=0)
	tackle_ratio = models.FloatField(default=0)
	int_per_90 = models.FloatField(default=0)
	dribbles_per_90 = models.FloatField(default=0)
	pass_completion = models.FloatField(default=0)
	key_passes_per_90 = models.FloatField(default=0)
	cr_c = models.IntegerField(default=0)
	shots_per_90 = models.FloatField(default=0)
	shot_percent = models.IntegerField(default=0)
	pom = models.IntegerField(default=0)
	reds = models.IntegerField(default=0)
	yellows = models.IntegerField(default=0)
	best_role = models.CharField(max_length=30, default="na")
	max_value = models.FloatField(default=0)
	home_grown_status = models.BooleanField(default=False)

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
	goals_per_90 = models.FloatField()
	assists_per_90 = models.FloatField()
	int_per_90 = models.FloatField()
	tackles_per_90 = models.FloatField()
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
