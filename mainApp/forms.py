from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class CreateSaveForm(forms.Form):
    team = forms.CharField(max_length=150)
    height_choice = forms.ChoiceField(choices = [("cm",'centimeters'), ("m",'meters'), ("ft",'feet')])
    wage_period = forms.ChoiceField(choices = [("weekly",'weekly'), ("monthly",'monthly'), ("yearly",'yearly')])
    distance_choice = forms.ChoiceField(choices=[("km",'km'), ("miles",'miles')])
    