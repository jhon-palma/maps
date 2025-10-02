import json
import os
import pdb
import random
import string
from datetime import date

import django
from django.shortcuts import get_object_or_404

from apps.shopmaps.models.stores import Categories, City, Project, State
from config.settings import local

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

BASE_DIR = os.path.join(local.BASE_DIR, 'deploy/json')

def insert_data():

    # country, created = Country.objects.get_or_create(name='Colombia')
    with open(os.path.join(BASE_DIR, 'state.json'), encoding='utf8') as json_file:
        for item in json.load(json_file):
            state = State()
            state.code = item['code']
            state.name = item['name']
            state.iso_code = item['iso_code']
            state.save()

    with open(os.path.join(BASE_DIR, 'cities.json'), encoding='utf8') as json_file:
        for item in json.load(json_file):
            city = City()
            city.state = State.objects.get_or_create(name=item['state'])[0]
            # city.code = item['code']
            city.name = item['name']
            city.save()

    with open(os.path.join(BASE_DIR, 'categories.json'), encoding='utf8') as json_file:
        for item in json.load(json_file):
            category = Categories()
            category.cat_name = item['cat_name']
            category.save()

    with open(os.path.join(BASE_DIR, 'projects.json'), encoding='utf8') as json_file:
        for item in json.load(json_file):
            project = Project()
            project.project_name = item['project_name']
            project.save()
    
insert_data()