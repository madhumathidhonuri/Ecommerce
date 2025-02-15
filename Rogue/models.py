from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_type = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username}, Product: {self.product_type} ID: {self.product_id}, Quantity: {self.quantity}"


class ClothingItem(models.Model):
    image = models.ImageField(upload_to='all_clothing/')
    brandname = models.CharField(max_length=150)
    color = models.CharField(max_length=60)
    price = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.brandname}-{self.color}-₹{self.price}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    product = GenericForeignKey('product_type', 'product_id')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product} ({self.quantity})"
class TShirts(ClothingItem):
    image=models.ImageField(upload_to='all_tshirts')

class Shirts(ClothingItem):
    image=models.ImageField(upload_to='all_shirts')

class Jeans(ClothingItem):
    image=models.ImageField(upload_to='all_jeans')


class Formals(ClothingItem):
    image=models.ImageField(upload_to='all_formals')


class Jackets(ClothingItem):
    image=models.ImageField(upload_to='all_jackets')


class Hoodies(ClothingItem):
    image=models.ImageField(upload_to='all_hoodies')


class Cargos(ClothingItem):
    image=models.ImageField(upload_to='all_cargos')
    
class Trousers(ClothingItem):
    image=models.ImageField(upload_to='all_trousers')


class Footwear(models.Model):
    image=models.ImageField(upload_to='all_footwear')
    brandname=models.CharField(max_length=150)
    price=models.IntegerField()
    def __str__(self):
        return f"{self.brandname}-₹{self.price}"

class Watches(models.Model):
    image = models.ImageField(upload_to='all_watches/')
    brandname = models.CharField(max_length=150)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.brandname}-₹{self.price}"

class Glasses(models.Model):
    image = models.ImageField(upload_to='all_glasses/')
    brandname = models.CharField(max_length=150)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.brandname}-₹{self.price}"
