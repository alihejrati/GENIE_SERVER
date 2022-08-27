from . import models
from utils import admin as Admin
from django.contrib import admin

# Register your models here.

Admin.register_all(
    __file__, 
    use_fsharp_for_all_at_first=True
    # admin_cfgs={
    #     'product': {
    #         # 'ignore': True,
    #         'list_display': ['f#', 'id', 'inv_status', 'price', 'col_title'], 
    #         'list_editable': ['price'],
    #         'list_per_page': 50,
    #         'ordering': ['id'],
    #         'list_select_related': ['collection'],
    #         'computed_columns': {
    #             'inv_status': admin.display(
    #                 description='علامت',
    #                 ordering='inventory', 
    #                 function=lambda self, product: str(product.inventory) + ' | ' + ('مثبت' if product.inventory > 0 else 'منفی')
    #             ),
    #             'col_title': admin.display(
    #                 description='col - title',
    #                 ordering='collection__title', 
    #                 function=lambda self, product: product.collection.title
    #             ),
    #         },
    #         'rename_columns': {
    #             'id': 'شناسه',
    #             # 'inv_status': 'new_name'
    #         }
    #     },
    #     'customer': {
    #         'list_editable': ['membership'],
    #         'ordering': ['first_name', '-id']
    #     },
    #     'order': {
    #         'list_display': ['f#', 'id', 'payment_status', 'customer_fullname', 'zip'],
    #         'list_select_related': ['customer', 'customer__address'],
    #         'list_per_page': 100,
    #         'computed_columns': {
    #             'customer_fullname': admin.display(
    #                 description='fullname',
    #                 ordering='customer__first_name', 
    #                 function=lambda self, row: row.customer.first_name + ' ' + row.customer.last_name 
    #             ),
    #             'zip': admin.display(
    #                 description='zip',
    #                 ordering='customer__address__zip', 
    #                 function=lambda self, row: row.customer.address.zip
    #             ),
    #         }
    #     }
    # }
)


from utils.html import PREDEFINED_HTML 
from utils.render import html
Admin.register('t0', models.Product, {
    'proxy': True,
    'list_per_page': 5,
    'list_display': ['id'],
    'computed_columns': {
        'f#': admin.display(
            description='',
            ordering='id',
            function=lambda self, row: html({'self': self, 'row': row, 'html_params': {
                'fsharp_delBtn': 'del',
                **{
                    'fsharp_btn': html({}, '<i title="setting" class="fa fa-cog" aria-hidden="true"></i>')
                }
            }}, PREDEFINED_HTML['f#setting'])
        )
    }
}, add_fshrp_at_first=True)

Admin.register('t1', models.Order, {
    'proxy': True,
    'list_per_page': 10,
    'list_display': ['id', 'payment_status', 'customer_fullname', 'zip'],
    'list_select_related': ['customer', 'customer__address'],
    'computed_columns': {
        'customer_fullname': admin.display(
            description='fullname',
            ordering='customer__first_name', 
            function=lambda self, row: row.customer.first_name + ' ' + row.customer.last_name 
        ),
        'zip': admin.display(
            description='zip',
            ordering='customer__address__zip', 
            function=lambda self, row: row.customer.address.zip
        ),
    },
    'meta': {
        'verbose_name_plural': 't1-name',
    }
})