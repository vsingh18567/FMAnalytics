from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class CreateSaveForm(forms.Form):
    team = forms.CharField(max_length=150)
    height_choice = forms.ChoiceField(choices = [(1,'centimeters'), (2,'meters'), (3,'feet')])
    wage_period = forms.ChoiceField(choices = [(1,'weekly'), (2,'monthly'), (3,'yearly')])
    distance_choice = forms.ChoiceField(choices=[(1,'km'), (2,'miles')])
    