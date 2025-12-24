from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .permissions import IsAdmin, IsRestaurantOwner, IsCustomer, IsOwnerOrReadOnly
from rest_framework.authtoken.models import Token

from .models import Restaurant, MenuCategory, MenuItem, Order, OrderItem
from .serializers import (
    RestaurantSerializer,
    MenuCategorySerializer,
    MenuItemSerializer,
    OrderSerializer,
    OrderItemSerializer
)
from .serializers import RegisterSerializer, LoginSerializer



class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# USER LOGIN
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            "message": "Login successful",
            "access": access,
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        }, status=status.HTTP_200_OK)



# USER LOGOUT
class LogoutAPIView(generics.GenericAPIView):
    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

#List & create restaurants
class RestaurantListCreateAPIView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(
            {
                "message": "Restaurant created successfully",
                "status": "success",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

#Update or destroy restaurants created
class RestaurantRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner, IsOwnerOrReadOnly,]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Restaurant updated successfully",
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"status": "success", "message": "Restaurant deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
#MenuCategory views
class MenuCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    permission_classes = [IsAdmin, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Category created successfully",
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

#Create a menu item
class MenuItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsRestaurantOwner, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Menu item created successfully",
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


#Update or destroy menu items created
class MenuItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


#Create an order 
class OrderItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsCustomer]

#OrderList views
class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(customer=self.request.user)
            return Response(
                {
                    "message": "Order created successfully",
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


#Update or destroy an order
class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Order updated successfully",
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )




