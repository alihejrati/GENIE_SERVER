from .render import html, URL
from .html import PREDEFINED_HTML
from django.contrib import admin

PREDEFINED_COMPUTED_COLUMNS = {}

index = 'f#btns'
PREDEFINED_COMPUTED_COLUMNS [index] = lambda html_params, index=index, handle={}: admin.display(
    description=handle.get('description', ''),
    # ordering=handle.get('ordering', 'id'),
    function=lambda self, row, handle=handle: html({'index': index, 'self': self, 'row': row, 'html_params': {
        f'{index}:editBtn': html({}, '<i class="fa fa-pencil" aria-hidden="true"></i>'),
        f'{index}:delBtn':  html({}, '<i class="fa fa-trash" aria-hidden="true"></i>'),
        f'{index}:viewBtn': html({}, '<i class="fa fa-eye" aria-hidden="true"></i>'),
        f'{index}:editHref': URL('change', self, row),
        f'{index}:delHref':  URL('del', self, row),
        f'{index}:viewHref': URL('view', self, row),
        **html_params
    }}, PREDEFINED_HTML[index])
)

index = 'f#link'
PREDEFINED_COMPUTED_COLUMNS [index] = lambda html_params, index=index, handle={}: admin.display(
    description=handle.get('description', ''),
    # ordering=handle.get('ordering', 'id'),
    function=lambda self, row, handle=handle: html({'index': index, 'self': self, 'row': row, 'html_params': {
        f'{index}:href': handle.get('seturl', lambda s, r: '#')(self, row),
        f'{index}:jumpBtn': html({}, '<i class="fa fa-external-link" aria-hidden="true"></i>'),
        **html_params
    }}, PREDEFINED_HTML[index])
)