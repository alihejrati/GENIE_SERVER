from utils import crud
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import QuerySet, ExpressionWrapper, Q, F, Value, Count, Max, Min, Avg, Sum, DecimalField
from apps.store.models import Product, Customer, Collection, Order, OrderItem, Promotion
from apps.tags.models import TaggedItem

# from django.db.models.functions import MD5, Concat
# Create your views here.

def say_hello(req):
    res = {}
    qs = []

    # qs = Product.objects.annotate(
    #     new_price=ExpressionWrapper(F('price') * .8, output_field=DecimalField(max_digits=6, decimal_places=2))
    # )
    # res = ''

    # qs = Order.objects \
    # .select_related('customer') \
    # .prefetch_related('orderitem_set__product') \
    # .annotate(order_count=Count('orderitem')) \
    # .order_by('-created_at')[:5]

    # res = qs.aggregate(orderitem_max_price=Max('orderitem__unit_price'), max_price=Max('orderitem__product__price'))

    return render(req, 'test.html', {
        'data': list(qs),
        'name': res
    })
    # return HttpResponse('hoooooooooooooooOO!!')
