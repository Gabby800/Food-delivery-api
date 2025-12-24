from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RestaurantListCreateAPIView, RestaurantRetrieveUpdateDestroyAPIView,
    MenuCategoryListCreateAPIView,
    MenuItemListCreateAPIView, MenuItemRetrieveUpdateDestroyAPIView,
    OrderItemListCreateAPIView,
    OrderListCreateAPIView, OrderRetrieveUpdateDestroyAPIView, RegisterAPIView, LoginAPIView, LogoutAPIView
)


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    path("auth/register/", RegisterAPIView.as_view()),
    path("auth/login/", LoginAPIView.as_view()),
    path("auth/logout/", LogoutAPIView.as_view()),

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