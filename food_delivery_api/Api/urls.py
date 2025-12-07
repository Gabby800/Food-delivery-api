from django.urls import path
from .views import (
    RestaurantListCreateAPIView, RestaurantRetrieveUpdateDestroyAPIView,
    MenuCategoryListCreateAPIView,
    MenuItemListCreateAPIView, MenuItemRetrieveUpdateDestroyAPIView,
    OrderItemListCreateAPIView,
    OrderListCreateAPIView, OrderRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    # Restaurants
    path("restaurants/", RestaurantListCreateAPIView.as_view()),
    path("restaurants/<int:pk>/", RestaurantRetrieveUpdateDestroyAPIView.as_view()),

    # Categories
    path("categories/", MenuCategoryListCreateAPIView.as_view()),
    
    # MenuItems
    path("menu-items/", MenuItemListCreateAPIView.as_view()),
    path("menu-items/<int:pk>/", MenuItemRetrieveUpdateDestroyAPIView.as_view()),
    
    # OrderItems
    path("order-items/", OrderItemListCreateAPIView.as_view()),
    path("orders/", OrderListCreateAPIView.as_view()),

    #Orders
    path("orders/<int:pk>/", OrderRetrieveUpdateDestroyAPIView.as_view()),
]