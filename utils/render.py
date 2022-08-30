import os
from django.urls import reverse
from django.template import Context, Template
from django.utils.html import urlencode

def URL(page, self, row):
    # if page == 'ManyToManyField':
    #     s = self
    #     r = row
    #     return os.path.join(
    #         reverse(f'admin:{s.app_label}_{s.model_name}_changelist'),
    #         '?' + urlencode({f'{s.filter}': r.id})
    #     )

    if page == 'ManyToOneRel':
        s = self
        r = row
        return os.path.join(
            reverse(f'admin:{s.app_label}_{s.model_name}_changelist'),
            '?' + urlencode({f'{s.filter}': r.id})
        )

    if page == 'change':
        return os.path.join(
            reverse(f'admin:{self.my_vars.model._meta.app_label}_{self.my_vars.model_name}_changelist'),
            str(row.id),
            'change'
        )
    if page == 'del':
        return os.path.join(
            reverse(f'admin:{self.my_vars.model._meta.app_label}_{self.my_vars.model_name}_changelist'),
            str(row.id),
            'delete'
        )
    if page == 'view':
        return os.path.join(
            reverse(f'admin:{self.my_vars.model._meta.app_label}_{self.my_vars.model_name}_changelist'),
            '?' + urlencode({'id': row.id})
        )

def html(obj_dict_pure, html_like):
    index = obj_dict_pure.get('index', '')
    obj_dict = dict(obj_dict_pure)
    _html_params = obj_dict.get('html_params', {})
    html_params = {}

    for key in _html_params:
        K = key.split(':')
        if len(K) == 2 and K[0] == index and K[1] != '':
            html_params[K[1]] = _html_params[key]

    obj_dict['html_params'] = html_params

    t = Template(html_like)
    c = Context(obj_dict)
    return t.render(c)