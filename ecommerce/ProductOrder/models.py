from django.db import models
from django.db.models.fields import related
from UserLogin.models import User
# Create your models here.
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, default=1)
    description = models.TextField(
        max_length=200, default='', null=True, blank=True)
    image = models.ImageField(verbose_name="Product Image")
    quantity = models.IntegerField(default=0, verbose_name="Product Quantity")

    created_at = models.DateTimeField(
        null=True, blank=True, default=timezone.now())
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(
        null=True, blank=True, default=timezone.now())
    updated_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="+")

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey("Product",
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        null=True, blank=True, default=timezone.now())

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
