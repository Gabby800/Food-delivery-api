from rest_framework import serializers
from .models import Restaurant, MenuCategory, MenuItem, Order, OrderItem, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = '__all__'
    
    def get_price_with_tax(self, obj):
        return obj.price * 15.80


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
<<<<<<< HEAD
        model = Order
=======
        model = Order
        fields = '__all__'
>>>>>>> 090a9e81d413a03b3f836426b84d59c1c4d148df
