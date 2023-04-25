from django.urls import path
from . import views
from .views import cart_add



urlpatterns = [
 path('base/',views.BASE, name='base'),
 path('index/',views.INDEX, name='index'),
 path('products/',views.PRODUCT, name='product'),
 path('search/', views.SEARCH, name='search'),
 path('products/<str:id>',views.PRODUCT_DETAIL_PAGE, name='product_detail'),
 path('checkout/', views.Check_out, name='checkout'),
 path('success/',views.success, name='success'),
 path('wishlist/',views.WISHLIST, name='wishlist'),
 path('aboutus/',views.Aboutus, name='aboutus'),
 # cart
 path('add/<int:id>/', views.cart_add, name='cart_add'),
 path('item_clear/<int:id>/', views.item_clear, name='item_clear'),
 path('item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
 path('item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
 path('cart_clear/', views.cart_clear, name='cart_clear'),
 path('cart_details/',views.cart_detail,name='cart_detail'),
 path('checkout/placeorder/', views.PLACE_ORDER, name='placeorder'),
 


 

]