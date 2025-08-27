from .models import *
from django.contrib import admin

admin.site.register(Supermarket)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(HistoryPrice)
admin.site.register(ShoppingList)
admin.site.register(ShoppingItem)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)