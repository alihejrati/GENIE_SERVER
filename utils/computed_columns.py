from .render import html
from .html import PREDEFINED_HTML
from django.contrib import admin

PREDEFINED_COMPUTED_COLUMNS = {}

PREDEFINED_COMPUTED_COLUMNS ['f#'] = lambda html_params: admin.display(
    description='',
    # ordering='id',
    function=lambda self, row: html({'self': self, 'row': row, 'html_params': {
        'fsharp_editBtn': html({}, '<i class="fa fa-pencil" aria-hidden="true"></i>'),
        'fsharp_delBtn':  html({}, '<i class="fa fa-trash" aria-hidden="true"></i>'),
        'fsharp_viewBtn': html({}, '<i class="fa fa-eye" aria-hidden="true"></i>'),
        **html_params
    }}, PREDEFINED_HTML['f#'])
)