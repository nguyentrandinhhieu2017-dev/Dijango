from django.contrib import admin
from .models import Category, Book, Purchase, Wallet


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "stock", "category")
    list_filter = ("category",)
    search_fields = ("title", "author")
    list_editable = ("price", "stock")
    list_per_page = 20


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "purchased_at")
    list_filter = ("purchased_at", "user")
    search_fields = ("user__username", "book__title")
    list_per_page = 20


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "updated_at")
    search_fields = ("user__username", "user__email")
    list_editable = ("balance",)
    list_per_page = 20
