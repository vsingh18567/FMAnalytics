from django import forms
from .models import Save, Season

class NewSeasonForm(forms.Form):
	season_end_year = forms.IntegerField()
	division = forms.IntegerField()
	position = forms.IntegerField()
	teams_in_league = forms.IntegerField()
	notes = forms.CharField(widget=forms.Textarea, max_length=4000, required=False)
	file = forms.FileField()


class CreateSaveForm(forms.Form):
	team = forms.CharField(max_length=150)

class EditSeasonForm(forms.Form):
	season_end_year = forms.IntegerField()
	division = forms.IntegerField()
	position = forms.IntegerField()
	teams_in_league = forms.IntegerField()
	notes = forms.CharField(widget=forms.Textarea, max_length=4000, required=False)
