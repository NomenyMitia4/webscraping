from django import forms
from .models import Pays

class PaysForm(forms.ModelForm):
    class Meta:
        model = Pays
        fields = '__all__'
        labels = {
            'product_id': 'Product ID',
            'nom': 'Nom du pays'
        },
        widgets = {
            'product_id': forms.NumberInput(
                attrs={'placehoder':'e.g 1', 'class':'form-control'}),
            'nom': forms.TextInput(
                attrs={'placeholder':'e.g Madagascar', 'class':'form-control'})
        }