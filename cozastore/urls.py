from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainapp import views



admin.site.site_header = "COZASTORE"
admin.site.site_title = "COZASTORE Admin Portal"
admin.site.index_title = "Welcome to COZASTORE Admin Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.home),
    path("shop/<str:mc>/<str:sc>/",views.shop),
    path("price-filter/<str:mc>/<str:sc>/",views.pricefilter),
    path("sort-filter/<str:mc>/<str:sc>/",views.sortfilter),
    path("product-detail/<int:num>/",views.productDetail),
    path('search/',views.search),
    path('checkout/',views.checkout),
    path("blog/",views.blog),
    path("about/",views.about),
    path("contact/",views.contact),
    path("login/",views.loginpage),
    path("logout/",views.logoutpage),        
    path("signup/",views.signuppage),
    path("profile/",views.profilepage),
    path("update-profile/",views.update_profile),
    path("add_to_cart/<int:num>/",views.addtocart),
    path("cart/",views.cart),
    path("update_cart/<str:id>/<str:op>/",views.updatecart),
    path("delete_cart/<str:id>/",views.deletecart),
    path("place_order/",views.placeorder),
    path("confirmation/",views.confirm),
    path("wishlist/",views.wishlist),
    path("add_to_wishlist/<int:num>/",views.addtowishlist),
    path("delete_wishlist/<int:num>",views.deletewishlist),
    path("forgotpw-1/",views.forgotpw1),
    path("forgotpw-2/",views.forgotpw2),
    path("forgotpw-3/",views.forgotpw3),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
