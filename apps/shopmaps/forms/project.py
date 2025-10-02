from django import forms

from apps.shopmaps.models.stores import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control text-uppercase'}),
        }
        labels = {
            'project_name':'Proyecto',
        }
