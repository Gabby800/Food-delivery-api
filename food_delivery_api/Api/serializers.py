from rest_framework import serializers
from .models import Restaurant, MenuCategory, MenuItem, Order, OrderItem

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    category = MenuCategorySerializer(read_only=True)
    price_with_tax = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = '__all__'
    
    def get_price_with_tax(self, obj):
        return obj.price * 


class OrderItemSerializer(serializers.ModelSerializer):
    item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'