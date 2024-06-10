import imp
import datetime
from tkinter import CASCADE
from unicodedata import category
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class SharedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        abstract = True
    
# Create your models here.
class Category(SharedModel):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Product(SharedModel):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    qty = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    
    def __str__(self):
        return f"{self.name} (price{self.price})"      
    
class Customer(SharedModel):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length =50)
    last_name = models.CharField(max_length = 50)
    contact = models.DateField(default=datetime.date.today)
    address = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    

class Cart(SharedModel):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    
    def __str__(self):
        return f"{self.customer}"

class CartItem(SharedModel):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='cart_items' )
    product = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name = 'product_items')
    qty = models.PositiveIntegerField()
    
    
    def __str__(self):
        return self.product
    
    def __str__(self):
        return f"{self.cart.customer} ({self.product})"
    
class order(SharedModel):
    
    
    ORDER_PENDING_CHOICE = 'PENDING'
    ORDER_INDELIVERY_CHOICE = 'INDELIVERY'
    ORDER_COMPLETED_CHOICE = 'COMPLETED'
    ORDER_STATUS = [
        (ORDER_PENDING_CHOICE, 'PENDING'),
        (ORDER_INDELIVERY_CHOICE, 'INDELIVERY'),
        (ORDER_COMPLETED_CHOICE,'COMPLETED'),
    ]
    
    
    PAYMENT_MODE_KHALTI = 'KHALTI'
    PAYMENT_MODE_COD = 'COD'
    PAYMENT_MODE =[
        (PAYMENT_MODE_KHALTI,'KHALTI'),
        (PAYMENT_MODE_COD,'COD'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models. PROTECT)
    address = models.CharField(max_length= 225, null = True, blank= True)
    payment_status = models.BooleanField(default = False)
    payment_mode = models.CharField(choices = PAYMENT_MODE,max_length = 255)
    status = models.CharField(choices = ORDER_STATUS, default= ORDER_PENDING_CHOICE, max_length= 255)
    
    
    def __str__(self):
        return f"OrderID #{self.pk}"
    
class OrderItem(SharedModel):
    order = models.ForeignKey(Cart,on_delete=models.PROTECT, related_name='order_items' )
    product = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='product_order_items')
    qty = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    def __str__(self):
        return self.product
    
    