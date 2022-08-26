from utils import admin as Admin
from django.contrib import admin

# Register your models here.

Admin.register_all(__file__, admin_cfg={
    'product': {
        'list_display': ['title', 'price', 'id'],
        'list_editable': ['price'],
        'list_per_page': 5,
        'ordering': ['id']
    },
    'customer': {
        'list_editable': ['membership'],
        'ordering': ['first_name', '-id']
    }
})