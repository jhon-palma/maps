from django import forms

from apps.shopmaps.models.stores import Categories

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['cat_name', 'cat_icon']
        widgets = {
            'cat_name': forms.TextInput(attrs={'class': 'form-control text-uppercase'}),
            'cat_icon': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cat_name':'Categoria',
            'cat_icon':'Icono',
        }
