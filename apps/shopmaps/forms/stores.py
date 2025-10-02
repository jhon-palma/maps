from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from django.urls import reverse_lazy

from apps.shopmaps.models.stores import City, Images, Project, State, StoreProject, Stores


class StoreForm(forms.ModelForm):
    state = forms.ModelChoiceField(
        queryset=State.objects.all().order_by('name'),
        widget=forms.Select(attrs={"class": "form-control", "data-url": reverse_lazy("maps:ajax_load_cities"),}),
        required=True,
        label="Estado"
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        label="Ciudad"
    )
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all().order_by("project_name"),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        required=True,
        label="Proyecto"
    )
    class Meta:
        model = Stores
        fields = [
            'name',
            'address',
            'city',
            'zip_code',
            'cat_id',
            'status_store',
            'image',
            'image1',
            'image2',
            'image3',
            'image4',
            'mobile',
            'pos_contact',
            'email',
            'distributor_1',
            'distributor_2',
            'nombre_tendero',
            'description',
            'latitude',
            'longitude',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control text-uppercase'}),
            'address': forms.TextInput(attrs={'class': 'form-control text-uppercase'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'cat_id': forms.Select(attrs={"class": "form-control"}),
            'status_store': forms.Select(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'image': forms.Select(attrs={"class": "form-control"}),
            'image1': forms.Select(attrs={"class": "form-control"}),
            'image2': forms.Select(attrs={"class": "form-control"}),
            'image3': forms.Select(attrs={"class": "form-control"}),
            'image4': forms.Select(attrs={"class": "form-control"}),
            'mobile': forms.TextInput(attrs={"class": "form-control"}),
            'pos_contact': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'distributor_1': forms.TextInput(attrs={"class": "form-control"}),
            'distributor_2': forms.TextInput(attrs={"class": "form-control"}),
            'nombre_tendero': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={'rows': 3, "class": "form-control"}),
            'latitude': forms.TextInput(attrs={"class": "form-control"}),
            'longitude': forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            'name':'Nombre de la tienda',
            'address':'Dirección',
            'zip_code': 'Código Postal',
            'cat_id': 'Categoria',
            'status_store': 'Estado de la tienda',
            'mobile': 'Teléfono',
            'email': 'Correo electrónico',
            'distributor_1': 'Distribuidor 1',
            'distributor_2': 'Distribuidor 2',
            'nombre_tendero': 'Nombre Tendero',
            'description': 'Descripción',
            'latitude': 'Latitud',
            'longitude': 'Longitud',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].required = True
        if self.instance and self.instance.pk:
            # Poblar proyectos
            self.fields['projects'].initial = Project.objects.filter(
                storeproject__store=self.instance
            )

        if "state" in self.data:
            try:
                state_id = int(self.data.get("state"))
                self.fields["city"].queryset = City.objects.filter(state_id=state_id)
            except (ValueError, TypeError):
                self.fields["city"].queryset = City.objects.none()
        elif self.instance and self.instance.pk and getattr(self.instance, "city", None):
            self.fields["state"].initial = self.instance.city.state
            self.fields["city"].queryset = City.objects.filter(state=self.instance.city.state)
        else:
            self.fields["city"].queryset = City.objects.none()
    
    def clean_city(self):
        city = self.cleaned_data.get("city")
        return city

    def save(self, commit=True):
        store = super().save(commit=commit)

        if commit:
            selected_projects = self.cleaned_data.get('projects')

            StoreProject.objects.filter(store=store).delete()

            for project in selected_projects:
                StoreProject.objects.create(store=store, project=project)

        return store


class ImageForm(forms.ModelForm):
    SCORE_CHOICES = [("", "--------------")] + [(i, str(i)) for i in range(1, 6)]
    points = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.Select(attrs={"class": "form-control"}), label="Puntaje Imagen", required=False )
    class Meta:
        model = Images
        fields = ['file', 'points']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'file': 'Imagenes',
        }

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")
        points = cleaned_data.get("points")

        if file and not points:
            self.add_error("points", "El puntaje es obligatorio si subes una imagen.")
        return cleaned_data

ImageFormSet = inlineformset_factory(
    Stores,
    Images,
    form=ImageForm,
    extra=1,
    can_delete=True
)