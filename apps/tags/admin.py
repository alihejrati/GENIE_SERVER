from . import models
from utils import admin as Admin
from django.contrib import admin
from django.db.models import QuerySet, ExpressionWrapper, Q, F, Value, Count, Max, Min, Avg, Sum, DecimalField

# Register your models here.

Admin.register_all(
    __file__, 
    # IfsharpBtns=0,
    admin_cfgs={
    }
)