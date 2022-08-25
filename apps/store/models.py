from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Product(models.Model):
    # sku = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2) # 9999.99
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    products = models.ManyToManyField(Product, related_name='promotions')

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255, null=False, blank=False, unique=True)
    birth_date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    membership = models.CharField(max_length=1, default='B', choices=[
        ('B', 'Bronze'),
        ('S', 'Silver'),
        ('G', 'Gold'),
    ])

class Address(models.Model):
    zip = models.CharField(max_length=255, unique=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(null=True, auto_now_add=False, auto_now=True)
    payment_status = models.CharField(max_length=1, default='P', choices=[
        ('P', 'Pending'),
        ('C', 'Compleate'),
        ('F', 'Failed'),
    ])
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()