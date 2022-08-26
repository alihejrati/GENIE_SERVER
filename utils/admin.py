from django.contrib import admin
from django.apps import apps as Apps

def register_all(
    f, 
    flag_sendName=False, 
    admin_cfg=None
):
    admin_cfg = {} if admin_cfg is None else admin_cfg
    app_name = f if flag_sendName else str(f).split('/')[-2]
    App = Apps.get_app_config(app_name)
    for model_name, model in App.models.items():
        _list_display = []
        for field in model._meta.get_fields():
            fn = field.name
            key_type = str(type(field)).replace("'", '').replace('>', '').split('.')[-1]
            if key_type == 'ManyToManyField':
                continue
            if key_type == 'ManyToOneRel':
                continue
            if key_type == 'ForeignKey':
                fn = fn + '_id'
            # if fn == '???':
            #     print('!!!!!!!!!!!!!!!', key_type)
            _list_display.append(fn)
        class DynamicModelAdmin(admin.ModelAdmin):
            list_display = admin_cfg.get(model_name, {}).get('list_display', _list_display)
            list_editable = admin_cfg.get(model_name, {}).get('list_editable', [])
            list_per_page = admin_cfg.get(model_name, {}).get('list_per_page', 10)
            ordering = admin_cfg.get(model_name, {}).get('ordering', [])

        admin.site.register(model, DynamicModelAdmin)