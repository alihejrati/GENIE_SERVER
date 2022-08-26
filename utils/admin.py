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
        if admin_cfg.get(model_name, {}).get('ignore', False):
            continue

        _list_display = []
        _ref_cols = {}
        
        for field in model._meta.get_fields():
            fn = field.name
            key_type = str(type(field)).replace("'", '').replace('>', '').split('.')[-1]
            
            if key_type == 'ManyToManyField':
                continue
            if key_type == 'ManyToOneRel':
                continue
            if key_type == 'ForeignKey':
                legacy_fn = fn
                fn = 'computed_column_' + legacy_fn + '_ID'
                _ref_cols[fn] = admin.display(
                    description=legacy_fn,
                    ordering=legacy_fn, 
                    function=lambda self, row, legacy_fn=legacy_fn: getattr(row, legacy_fn + '_id')
                )
            if key_type == 'OneToOneField':
                legacy_fn = fn
                fn = 'computed_column_' + legacy_fn + '_ID'
                _ref_cols[fn] = admin.display(
                    description=legacy_fn,
                    ordering=legacy_fn, 
                    function=lambda self, row, legacy_fn=legacy_fn: getattr(row, legacy_fn + '_id')
                )
            _list_display.append(fn)
        
        class DynamicModelAdmin(admin.ModelAdmin):
            list_display = admin_cfg.get(model_name, {}).get('list_display', _list_display)
            list_editable = admin_cfg.get(model_name, {}).get('list_editable', [])
            list_per_page = admin_cfg.get(model_name, {}).get('list_per_page', 10)
            ordering = admin_cfg.get(model_name, {}).get('ordering', [])
        
        for _ref_col_key in _ref_cols:
            setattr(DynamicModelAdmin, _ref_col_key, _ref_cols[_ref_col_key])
        
        computed_columns = admin_cfg.get(model_name, {}).get('computed_columns', {})
        for cc_key in computed_columns:
            setattr(DynamicModelAdmin, cc_key, computed_columns[cc_key])
        
        rename_columns = admin_cfg.get(model_name, {}).get('rename_columns', {})
        for rc_key in rename_columns:
            col = getattr(DynamicModelAdmin, rc_key, None)
            if col == None:
                col = getattr(model, rc_key, None)
                if col is not None:
                    col.field.verbose_name = rename_columns[rc_key]
                else:
                    pass
            else:
                col.short_description = rename_columns[rc_key]
        
        admin.site.register(model, DynamicModelAdmin)