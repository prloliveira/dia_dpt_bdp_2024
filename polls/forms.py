from django import forms
from .models import UserData

class DataCollectionForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['gender', 'birth_date', 'year_joined', 'unit_area', 'function']
        
    gender = forms.ChoiceField(choices=UserData.GENDER_CHOICES, required=True)
    unit_area = forms.ChoiceField(choices=UserData.DAS_CHOICES, required=True)
    function = forms.ChoiceField(choices=UserData.DAS_FUNCTION, required=True)