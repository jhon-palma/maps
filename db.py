# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    cat_name = models.CharField(max_length=100, db_collation='utf8_bin', blank=True, null=True)
    cat_icon = models.CharField(max_length=255, blank=True, null=True)
    cat_parent_id = models.IntegerField(blank=True, null=True)
    cat_free_flag = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Images(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'


class Project(models.Model):
    project_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'project'


class StoreProject(models.Model):
    store = models.ForeignKey('Stores', models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_project'


class Stores(models.Model):
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, db_collation='utf8_bin')
    address = models.CharField(max_length=255, db_collation='utf8_bin')
    ciudad = models.CharField(max_length=255, db_collation='utf8_bin')
    estado = models.CharField(max_length=255, db_collation='utf8_bin')
    zip_code = models.CharField(max_length=255, db_collation='utf8_bin')
    cat_id = models.CharField(max_length=255, db_collation='utf8_bin')
    status_tienda = models.CharField(max_length=255, db_collation='utf8_bin')
    temporada = models.CharField(max_length=255, db_collation='utf8_bin')
    image = models.CharField(db_column='IMAGE', max_length=255, db_collation='utf8_bin')  # Field name made lowercase.
    image2 = models.CharField(db_column='IMAGE2', max_length=255, db_collation='utf8_bin')  # Field name made lowercase.
    image3 = models.CharField(db_column='IMAGE3', max_length=255, db_collation='utf8_bin')  # Field name made lowercase.
    image4 = models.CharField(db_column='IMAGE4', max_length=255, db_collation='utf8_bin')  # Field name made lowercase.
    pos_contact = models.CharField(db_column='POS_contact', max_length=255, db_collation='utf8_bin')  # Field name made lowercase.
    telephone = models.CharField(max_length=25, blank=True, null=True)
    distributor_1 = models.CharField(max_length=255, db_collation='utf8_bin')
    distributor_2 = models.CharField(max_length=255, db_collation='utf8_bin')
    description = models.TextField(db_collation='utf8_bin', blank=True, null=True)
    fax = models.CharField(max_length=25, blank=True, null=True)
    mobile = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    embed_video = models.CharField(max_length=255, blank=True, null=True)
    default_media = models.CharField(max_length=255, blank=True, null=True)
    approved = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', related_name='stores_updated_by_set', blank=True, null=True)
    nombre_tendero = models.CharField(max_length=180, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stores'


class StoresImages(models.Model):
    stores = models.ForeignKey(Stores, models.DO_NOTHING)
    images = models.ForeignKey(Images, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'stores_images'


class Users(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    user_type = models.CharField(max_length=3, db_comment='Columna que define el tipo de usuario. Tipos de usuario: A= administrador del sistema. O= Operativo C= cliente D= Demo')

    class Meta:
        managed = False
        db_table = 'users'
