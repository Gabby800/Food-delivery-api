from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES =(
        ('admin', 'Admin'),
        ('restaurant_owner', 'Restaurant Owner'),
        ('customer', 'Customer')
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f'{self.username} ({self.role})'


# Restaurant owned by a user
class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=250)
    addres = models.TextField()
    phone = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name

#Menu category for a restaurant
class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

#Item in a menu category
class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    def __str__(self):
        return self.name
    
#  Customer order
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('CONFIRMED','Confirmed'),
        ('OUT_FOR_DELIVERY','Out for delivery'),
        ('DELIVERED','Delivered'),
        ('CANCELLED','Cancelled')
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateField(auto_now=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f'order {self.id}'

#Specific item in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.menu_item.name} x {self.quantity}'

