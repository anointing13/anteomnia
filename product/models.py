from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.apps import apps
from decimal import Decimal


# Category model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# Brand model
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# Product model (Base Model)
class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    units_in_stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    image2 = models.ImageField(null=True, blank=True, upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    expiry_date = models.DateField()
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(max_length=10000)
    is_hidden = models.BooleanField(default=False)

    def get_display_price(self):
        SpecialOffer = apps.get_model('product_special_offer', 'SpecialOffer')
        active_offer = SpecialOffer.objects.filter(
            product=self,
            offer_start_date__lte=timezone.now(),
            offer_end_date__gte=timezone.now()
        ).first()

        if active_offer:
            if hasattr(active_offer, 'discount') and active_offer.discount:
                return self.price * Decimal((100 - active_offer.discount) / 100)
            elif hasattr(active_offer, 'special_offer_price') and active_offer.special_offer_price:
                return active_offer.special_offer_price

        if self.discount:
            return self.price * Decimal((100 - self.discount) / 100)

        return self.price

    def clean(self):
        if self.expiry_date and self.expiry_date <= timezone.now().date():
            raise ValidationError('Expiry date must be in the future.')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


# Proxy Model for Hidden Products
class HiddenProduct(Product):
    class Meta:
        proxy = True  # This makes HiddenProduct a proxy model, inheriting Product's table

    @classmethod
    def get_hidden_products(cls, query=None):
        """Retrieve hidden products based on search query."""
        hidden_products = cls.objects.filter(is_hidden=True)
        if query:
            hidden_products = hidden_products.filter(name__icontains=query)
        return hidden_products


# Cart Model
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Cart of {self.user.email}"


# CartItem Model
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        from product_special_offer.models import SpecialOffer

        active_offer = SpecialOffer.objects.filter(
            product=self.product,
            offer_start_date__lte=timezone.now(),
            offer_end_date__gte=timezone.now()
        ).first()

        if active_offer:
            discount_price = self.product.price - (self.product.price * active_offer.discount_percentage / 100)
        else:
            discount_price = self.product.price

        return self.quantity * discount_price

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.get_display_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# Favorite Model
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def get_favorite_price(self):
        SpecialOffer = apps.get_model('product_special_offer', 'SpecialOffer')

        special_offer = SpecialOffer.objects.filter(
            product=self.product,
            offer_start_date__lte=timezone.now(),
            offer_end_date__gte=timezone.now()
        ).first()

        if special_offer:
            discount_amount = (self.product.price * special_offer.discount_percentage) / 100
            return self.product.price - discount_amount

        return self.product.price

    def __str__(self):
        return f"{self.user}'s favorite: {self.product.name}"


class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
    points = models.PositiveIntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}'s Wallet - {self.points} Points"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('PURCHASE_BONUS', 'Purchase Bonus'),
        ('BIG_PURCHASE_BONUS', 'Big Purchase Bonus'),
        ('LOGIN_BONUS', 'Login Bonus'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('PURCHASE', 'Purchase'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    points = models.IntegerField()
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.points} Points - {self.product.name if self.product else 'No Product'}"

class Withdrawal(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="withdrawals")
    full_name = models.CharField(max_length=100)
    mobile_money_number = models.CharField(max_length=15)
    points = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user.email} - {self.status} ({self.points} Points)"