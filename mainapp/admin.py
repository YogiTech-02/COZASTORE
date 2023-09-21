from django.contrib import admin
from .models import *

admin.site.register(
    (
    )
    ) 

@admin.register(Buyer)
class BuyereAdmin(admin.ModelAdmin):
    list_display = ("id","name","email","phone")

@admin.register(Maincategory)
class MaincategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name")


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name","maincategory","subcategory","color","size","baseprice","discount","finalprice","stock","pic1")

@admin.register(Checkoutproduct)
class CheckoutproductAdmin(admin.ModelAdmin):
    list_display = ("id","name")

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ("id","user","orderstatus","paymentstatus","paymentMode","totalamount","shippingamount","finalamount","time")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id","user","product")


@admin.register(ContactUS)
class ContactUSAdmin(admin.ModelAdmin):
    list_display = ("id","name","email","phone","subject","message","status")
