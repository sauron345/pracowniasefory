from django import forms
from .models import Item
from .validators import allow_only_images


class AddItemForm(forms.ModelForm):
    picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images])

    class Meta:
        model = Item
        fields = ['name', 'price', 'picture', 'category', 'description', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nazwa produktu',
            'category': 'Kategoria',
            'description': 'Opis',
            'price': 'Cena',
            'picture': 'Zdjęcie',
            'is_available': 'Czy chcesz żeby produkt był dostępny?',
        }

    def __init__(self, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs = {'rows': 7, 'class': 'form-control'}


class EditItemForm(forms.ModelForm):
    picture = forms.FileField(validators=[allow_only_images],
                              label='Obraz')

    class Meta:
        model = Item
        fields = ['name', 'price', 'picture', 'category', 'description', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nazwa produktu',
            'category': 'Kategoria',
            'description': 'Opis',
            'price': 'Cena',
            'picture': 'Zdjęcie',
            'is_available': 'Czy chcesz żeby produkt był dostępny?',
        }

    def __init__(self, *args, **kwargs):
        super(EditItemForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs = {'rows': 7, 'class': 'form-control'}
