import os
from django.db import models
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Categories(models.Model):
    cat_name = models.CharField(max_length=100)
    cat_icon = models.ImageField(upload_to='img/icons/', blank=True, null=True)
    cat_parent_id = models.IntegerField(blank=True, null=True)
    cat_free_flag = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.cat_name}"


class State(models.Model):
    code = models.CharField(max_length=10, verbose_name="Código")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    iso_code = models.CharField(max_length=10, verbose_name="Código ISO")

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name="Departamento/Estado", related_name="cities")
    code = models.CharField(max_length=10, verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Nombre Municipio")

    def __str__(self):
        return self.name


class Project(models.Model):
    project_name = models.CharField(max_length=255)

    def __str__(self):
        return self.project_name 


class StoreProject(models.Model):
    store = models.ForeignKey('Stores', on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)


class Stores(models.Model):
    STATUS_STORE_CHOICES = [
        ("1st Branding", "1st Branding"),
        ("Maintenance", "Maintenance"),
    ]
    IMAGES_COUNT = [
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.PositiveIntegerField(blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Ciudad')
    zip_code = models.CharField(max_length=255)
    cat_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    status_store = models.CharField(max_length=20, choices=STATUS_STORE_CHOICES, default="branding", verbose_name="Estado de la tienda")
    status = models.BooleanField(default=True)
    temporada = models.CharField(max_length=255)
    image = models.CharField(max_length=2, choices=IMAGES_COUNT, default="0", verbose_name="Imagenes Posters")
    image1 = models.CharField(max_length=2, choices=IMAGES_COUNT, default="0", verbose_name="Imagenes 5*5 Sticker")
    image2 = models.CharField(max_length=2, choices=IMAGES_COUNT, default="0", verbose_name="Imagenes 8*8 Sticker")
    image3 = models.CharField(max_length=2, choices=IMAGES_COUNT, default="0", verbose_name="Imagenes Flange")
    image4 = models.CharField(max_length=2, choices=IMAGES_COUNT, default="0", verbose_name="Colgarin")
    pos_contact = models.CharField(db_column='POS_contact', max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=25, blank=True, null=True)
    distributor_1 = models.CharField(max_length=255, blank=True, null=True)
    distributor_2 = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    fax = models.CharField(max_length=25, blank=True, null=True)
    mobile = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    embed_video = models.CharField(max_length=255, blank=True, null=True)
    default_media = models.CharField(max_length=255, blank=True, null=True)
    approved = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', related_name='stores_updated_by_set', blank=True, null=True)
    nombre_tendero = models.CharField(max_length=180, blank=True, null=True)

@receiver(pre_save, sender=Stores)
def set_code(sender, instance, **kwargs):
    if instance.code is None:
        last_store = Stores.objects.all().order_by('code').last()
        if last_store:
            instance.code = last_store.code + 1
        else:
            instance.code = 1


def store_image_upload_path(instance, filename):
    # extensión del archivo original
    ext = filename.split('.')[-1]

    # nombre de la tienda (limpio para archivo)
    store_name = instance.store.name.replace(" ", "_")

    # Obtener el último consecutivo de imágenes de esta tienda
    last_image = instance.store.images.order_by("-id").first()
    if last_image and last_image.file:
        # Intentar extraer el consecutivo del nombre del archivo
        try:
            last_filename = os.path.basename(last_image.file.name)
            last_consecutive = int(last_filename.split("-")[1])
        except (IndexError, ValueError):
            last_consecutive = 0
    else:
        last_consecutive = 0

    new_consecutive = last_consecutive + 1

    # Usar el campo "code" de la tienda
    store_code = instance.store.code or "000"

    # Generar nombre final
    filename = f"{store_name}-{new_consecutive}-{store_code}.{ext}"

    # Guardar en stores/images/
    return os.path.join("stores/images/", filename)


class Images(models.Model):
    name = models.CharField(max_length=100)
    file = models.ImageField(upload_to=store_image_upload_path, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    store = models.ForeignKey(Stores, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f"{self.store.name} - {self.name or 'Sin nombre'}"
    
    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)