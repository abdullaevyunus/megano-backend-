from django.contrib import admin
from .models import Product, Image, Review, Tag, Specification, Category, Subcategory, Sales, Order, OrderProduct, \
    Profile, Payment, Basket

# Register your models here.
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Specification)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Sales)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Profile)
admin.site.register(Payment)
admin.site.register(Basket)
