from django.contrib import admin
from django.apps import apps as Apps
from utils.render import URL
from types import SimpleNamespace
from .computed_columns import PREDEFINED_COMPUTED_COLUMNS
 

predefined_computed_columns = PREDEFINED_COMPUTED_COLUMNS

def create_proxy_model(proxy_name, proxy_model, cfg=None):
    cfg = {} if cfg is None else cfg
    
    class  Meta:
        proxy = True
    
    meta_var = cfg.get('meta', {})
    for meta_var_key in meta_var:
        setattr(Meta, meta_var_key, meta_var[meta_var_key])

    attrs = {'__module__': proxy_model.__module__, 'Meta': Meta}
    return type(proxy_name, (proxy_model,), attrs)

def register(
    model_name,
    model,
    admin_cfg,
    add_fshrp_at_first=False
):
    admin_cfg = {} if admin_cfg is None else admin_cfg

    if admin_cfg.get('ignore', False):
        return

    if admin_cfg.get('proxy', False):
        model = create_proxy_model(model_name, model, cfg=admin_cfg)

    _list_display = []
    _list_editable_force = []
    _ref_cols = {}
    
    for field in model._meta.get_fields():
        fn = field.name
        key_type = str(type(field)).replace("'", '').replace('>', '').split('.')[-1]
        
        if getattr(field, 'choices', None) is not None:
            _list_editable_force.append(fn)

        if key_type == 'OneToOneRel':
            continue
        if key_type == 'ManyToManyField':
            continue
        if key_type == 'ManyToOneRel':
            h = getattr(model, fn, 
                getattr(model, fn + '_set', dict()))
            h_app = str(getattr(h, 'field', '')).split('.')[0]
            _ref_cols[fn] = predefined_computed_columns['f#link']({}, handle={
                'description': fn,
                'seturl': lambda s, r, fn=fn: URL('ManyToOneRel', SimpleNamespace(**{
                    'app_label': h_app,
                    'model_name': fn,
                    'filter': model_name + '__id'
                }), r)
            })
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
        my_vars = SimpleNamespace(**{
            'model_name': model_name,
            'model': model
        })

        list_display = admin_cfg.get('list_display', _list_display)
        list_editable = admin_cfg.get('list_editable', [])
        list_per_page = admin_cfg.get('list_per_page', 21)
        ordering = admin_cfg.get('ordering', [])
        list_select_related = admin_cfg.get('list_select_related', [])

        def get_queryset(self, request):
            return admin_cfg.get('get_queryset', lambda qs: qs)(super().get_queryset(request)) 

        class Media:
            js = ('fontawesomefree/js/all.min.js',)    
            css = {
                'all': ('fontawesomefree/css/all.min.css',)
            }

    if add_fshrp_at_first:
        DynamicModelAdmin.list_display.insert(0, 'f#btns')

    for pd_cc_key in DynamicModelAdmin.list_display:
        if pd_cc_key in predefined_computed_columns:
            setattr(DynamicModelAdmin, pd_cc_key, predefined_computed_columns[pd_cc_key](admin_cfg.get('html_params', {})))
        if (pd_cc_key in _list_editable_force) and (pd_cc_key not in DynamicModelAdmin.list_editable):
            print('@@@@@@@@@@@@@@@@@@2', pd_cc_key)
            DynamicModelAdmin.list_editable.append(pd_cc_key)


    for _ref_col_key in _ref_cols:
        setattr(DynamicModelAdmin, _ref_col_key, _ref_cols[_ref_col_key])
    
    computed_columns = admin_cfg.get('computed_columns', {})
    for cc_key in computed_columns:
        setattr(DynamicModelAdmin, cc_key, computed_columns[cc_key])
    
    rename_columns = admin_cfg.get('rename_columns', {})
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

def register_all(
    f, 
    use_fsharp_for_all_at_first=False,
    flag_sendName=False, 
    admin_cfgs=None
):
    admin_cfgs = {} if admin_cfgs is None else admin_cfgs
    app_name = f if flag_sendName else str(f).split('/')[-2]
    App = Apps.get_app_config(app_name)
    
    for model_name, model in App.models.items():
        register(
            admin_cfg=admin_cfgs.get(model_name, None),
            model_name=model_name,
            model=model,
            add_fshrp_at_first=use_fsharp_for_all_at_first
        )