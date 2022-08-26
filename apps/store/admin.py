from utils import admin as Admin
from django.contrib import admin

# Register your models here.

Admin.register_all(__file__, admin_cfg={
    # 'product': {
    #     # 'ignore': True,
    #     'list_display': ['id', 'inv_status', 'price'], 
    #     'list_editable': ['price'],
    #     'list_per_page': 5,
    #     'ordering': ['id'],
    #     'computed_columns': {
    #         'inv_status': admin.display(
    #             description='علامت',
    #             ordering='inventory', 
    #             function=lambda self, product: str(product.inventory) + ' | ' + ('مثبت' if product.inventory > 0 else 'منفی')
    #         )
    #     },
    #     'rename_columns': {
    #         'id': 'شناسه',
    #         # 'inv_status': 'new_name'
    #     }
        
    # },
    # 'customer': {
    #     'list_editable': ['membership'],
    #     'ordering': ['first_name', '-id']
    # }
})