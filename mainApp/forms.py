from django import forms

class NewSeasonForm(forms.Form):
    season_end_year = forms.IntegerField()
    division = forms.IntegerField()
    position = forms.IntegerField()
    teams_in_league = forms.IntegerField()
    notes = forms.CharField(widget=forms.Textarea, max_length=4000, required=False)
    file = forms.FileField()

class CreateSaveForm(forms.Form):
    team = forms.CharField(max_length=150)
    height_choice = forms.ChoiceField(choices = [("cm",'centimeters'), ("m",'meters'), ("ft",'feet')])
    wage_period = forms.ChoiceField(choices = [("weekly",'weekly'), ("monthly",'monthly'), ("yearly",'yearly')])
    distance_choice = forms.ChoiceField(choices=[("km",'km'), ("miles",'miles')])
    