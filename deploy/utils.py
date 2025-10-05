import json
import logging
import os
import pdb
import random
import string
from datetime import date

import django
from django.shortcuts import get_object_or_404
from django.utils import timezone
from apps.accounts.models.accounts import CustomUser
from apps.shopmaps.models.stores import Categories, City, Images, Project, State, StoreProject, Stores
from config.settings import local

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

BASE_DIR = os.path.join(local.BASE_DIR, 'deploy/json')

def insert_data():

    # with open(os.path.join(BASE_DIR, 'state.json'), encoding='utf8') as json_file:
    #     for item in json.load(json_file):
    #         state = State()
    #         state.code = item['code']
    #         state.name = item['name']
    #         state.iso_code = item['iso_code']
    #         state.save()

    # with open(os.path.join(BASE_DIR, 'cities.json'), encoding='utf8') as json_file:
    #     for item in json.load(json_file):
    #         city = City()
    #         city.state = State.objects.get_or_create(name=item['state'])[0]
    #         # city.code = item['code']
    #         city.name = item['name']
    #         city.save()

    # with open(os.path.join(BASE_DIR, 'categories.json'), encoding='utf8') as json_file:
    #     for item in json.load(json_file):
    #         category = Categories()
    #         category.cat_name = item['cat_name']
    #         category.save()

    # with open(os.path.join(BASE_DIR, 'projects.json'), encoding='utf8') as json_file:
    #     for item in json.load(json_file):
    #         project = Project()
    #         project.project_name = item['project_name']
    #         project.save()
    # logging.basicConfig(filename='import_errors.log', level=logging.ERROR)

    # with open(os.path.join(BASE_DIR, 'stores.json'), encoding='utf8') as json_file:
    #     for item in json.load(json_file):
    #         try:
    #             store = Stores()
    #             store.latitude = item["latitude"]
    #             store.longitude = item["longitude"]
    #             store.name = item["name"]
    #             store.address = item["address"]
    #             store.city = City.objects.get(name__iexact=item['ciudad'].strip())
    #             store.zip_code = item["zip_code"]
    #             store.cat_id = Categories.objects.get(cat_name__iexact=item["cat_id"]) 
    #             store.status_store = item["status_tienda"] 
    #             store.temporada = item["temporada"]
    #             store.image = item["IMAGE"]
    #             store.image1 = item["IMAGE2"]
    #             store.image2 = item["IMAGE3"]
    #             store.image3 = item["IMAGE4"]
    #             store.pos_contact = item["POS_contact"]
    #             store.telephone = item["telephone"]
    #             store.distributor_1 = item["distributor_1"]
    #             store.distributor_2 = item["distributor_2"] 
    #             store.description = item["description"]
    #             store.fax = item["fax"]
    #             store.mobile = item["mobile"]
    #             store.email = item["email"]
    #             store.website = item["website"]
    #             store.embed_video = item["embed_video"]
    #             store.default_media = item["default_media"]
    #             store.approved = item["approved"]
    #             store.status = item["status"]
    #             store.created = timezone.make_aware(item["created"]) if item["created"] else None
    #             store.created_by = CustomUser.objects.get(username__iexact=item["created_by"])
    #             store.modified = timezone.make_aware(item["modified"]) if item["modified"] else None
    #             store.updated_by = CustomUser.objects.get(username__iexact=item["updated_by"]) if item.get("updated_by") else None
    #             store.nombre_tendero = item["nombre_tendero"]
    #             store.save()
    #             print("Tienda guardada")
    #         except Exception as e:
    #             # Capturamos el error y lo registramos en el log
    #             logging.error(f"Error al procesar la tienda {item.get('name', 'Desconocida')}: {e}")
    #             # También puedes imprimir el error si lo deseas ver directamente en la consola
    #             print(f"Error al procesar la tienda {item.get('name', 'Desconocida')}: {e}")

    # with open(os.path.join(BASE_DIR, 'images.json'), encoding='utf8') as json_file:
    #     for item in json.load(json_file):
    #         try:
    #             image = Images()
    #             image.name = item["name"]
    #             image.file = item["file"]
    #             image.points = item["points"]
    #             image.store = Stores.objects.get(id=item["store"])
    #             image.save()
    #         except Exception as e:
    #             # Capturamos el error y lo registramos en el log
    #             # También puedes imprimir el error si lo deseas ver directamente en la consola
    #             print(f"Error al procesar la tienda {item.get('name', 'Desconocida')}: {e}")
    
    with open(os.path.join(BASE_DIR, 'stores_projects.json'), encoding='utf8') as json_file:
        for item in json.load(json_file):
            try:
                store_project = StoreProject()
                store_project.project = Project.objects.get(id=item["project_id"])
                store_project.store = Stores.objects.get(id=item["store_id"])
                store_project.save()
            except Exception as e:
                # Capturamos el error y lo registramos en el log
                # También puedes imprimir el error si lo deseas ver directamente en la consola
                print(f"Error al procesar la tienda {item.get('name', 'Desconocida')}: {e}")
insert_data()