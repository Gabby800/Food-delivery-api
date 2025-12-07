# Models Documentation

from django.db import models
from django.contrib.auth import get_user_model

# Get the active User model (works for custom user models)
user = get_user_model()


# ------------------------------------------------------
# RESTAURANT MODEL
# ------------------------------------------------------
class Restaurant(models.Model):
    """
    Represents a restaurant owned by a user.

    Fields:
        owner (User): The user who owns the restaurant.
        name (str): Name of the restaurant.
        addres (str): Address of the restaurant. (NOTE: consider renaming to 'address')
        phone (str): Contact phone number of the restaurant.
    """

    owner = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='restaurant',
        help_text="Owner of this restaurant"
    )

    name = models.CharField(
        max_length=250,
        help_text="Name of the restaurant"
    )

    addres = models.TextField(
        help_text="Physical address of the restaurant"
    )

    phone = models.CharField(
        max_length=250,
        help_text="Phone number of the restaurant"
    )

    def __str__(self):
        """Return the restaurant name when converted to string."""
        return self.name


# ------------------------------------------------------
# MENU CATEGORY
# ------------------------------------------------------
class MenuCategory(models.Model):
    """
    Represents a category of items in a restaurant menu.
    Example: 'Drinks', 'Pizza', 'Desserts'

    Fields:
        restaurant: The restaurant to which this category belongs.
        name: Category name.
    """

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='categories',
        help_text="Restaurant that owns this menu category"
    )

    name = models.CharField(
        max_length=250,
        help_text="Name of the menu category"
    )

    def __str__(self):
        return self.name


# ------------------------------------------------------
# MENU ITEM
# ------------------------------------------------------
class MenuItem(models.Model):
    """
    Represents an individual item within a menu category.

    Fields:
        category: The category this item belongs to.
        name: Item name.
        description: Optional detailed description.
        price: Cost of the menu item.
        image: Optional image of the item.
    """

    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Category this menu item belongs to"
    )

    name = models.CharField(
        max_length=100,
        help_text="Name of the menu item"
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description of the item"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Price of the menu item"
    )

    image = models.ImageField(
        upload_to='menu_items/',
        blank=True,
        null=True,
        help_text="Optional image of the menu item"
    )

    def __str__(self):
        return self.name


# ------------------------------------------------------
# ORDER MODEL
# ------------------------------------------------------
class Order(models.Model):
    """
    Represents a customer's order.

    Fields:
        customer (User): The user placing the order.
        restaurant (Restaurant): The restaurant fulfilling the order.
        created_at (date): Timestamp when the order was created.
        total_price (decimal): Total cost of the order.
        status (str): Current order status (pending, confirmed, etc.).
    """

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('OUT_FOR_DELIVERY', 'Out for delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="Customer who placed the order"
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="Restaurant processing this order"
    )

    created_at = models.DateField(
        auto_now=True,
        help_text="Date when the order was created"
    )

    total_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Total price of all items in the order"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        help_text="Current status of the order"
    )

    def __str__(self):
        """Return a readable representation of the order."""
        return f'Order {self.id}'


# ------------------------------------------------------
# ORDER ITEM MODEL
# ------------------------------------------------------
class OrderItem(models.Model):
    """
    Represents an item inside an order.

    Fields:
        order: The order to which this item belongs.
        menu_item: The menu item being ordered.
        quantity: The number of units ordered.
        price: Price of the menu item at the time of ordering.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        help_text="Order this item belongs to"
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        help_text="Menu item being ordered"
    )

    quantity = models.PositiveIntegerField(
        help_text="Quantity of the menu item ordered"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Price of the menu item multiplied by quantity"
    )

    def __str__(self):
        """Readable name showing the menu item and quantity."""
        return f"{self.menu_item.name} x {self.quantity}"
