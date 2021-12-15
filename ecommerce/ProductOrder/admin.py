from django.contrib import admin
from .models import Product, Category, Order
from UserLogin.models import User
# Register your models here.
from django.utils import timezone


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ("name", "price", "category", 'quantity')

    fieldsets = (
        ('Product Details', {
            "fields": (
                "name", "category", "description", "image"
            ),
        }),
        ('Product Quantity', {
            "fields": (
                "price", "quantity",
            ),
        })
    )

    list_filter = ("category",)

    def save_model(self, request, obj, form, change):
        user = User.objects.filter(
            email=request.user)[0]
        if not obj.pk:
            obj.created_by = user
            obj.created_at = timezone.now()
        else:
            obj.updated_at = timezone.now()
            obj.updated_by = user

        obj.save()


class OrderAdmin(admin.ModelAdmin):

    list_display = ("product", "customer", "quantity", "created_at")

    list_filter = ("product", "customer",)

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
