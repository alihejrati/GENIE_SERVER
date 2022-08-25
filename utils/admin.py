from django.contrib import admin
from django.apps import apps as Apps

def register_all(f):
    app_name = str(f).split('/')[-2]
    App = Apps.get_app_config(app_name)
    for model_name, model in App.models.items():
        admin.site.register(model)