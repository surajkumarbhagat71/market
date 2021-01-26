from django.urls import path
from .views import *

app_name = "shop"


urlpatterns = [
    path('userregistations',UserRegistations.as_view(),name="user_registations"),
    path('login/',Login.as_view(),name="login"),
    path('logout',Logout.as_view(),name='logout'),

#------------------------------- Work --------------------------

    path('',Home.as_view(),name="home"),
    path('search',SearchProduct.as_view(),name = "search"),
    path('item_detail/<int:pk>',PorductDetail.as_view(),name="item_detail"),
    path('addtocart/<int:pk>',AddToCart.as_view(),name="addtocart"),
    path('order_sumary/',OrderSumary.as_view(),name="order_sumary"),
    path('remove_item/<int:pk>',RemoveItemQty.as_view(),name="remove_item"),
    path('remove/<int:pk>',RemoveItem.as_view(),name="remove"),
    path('checkout',Checkout.as_view(),name = 'checkout'),
    path('update/<int:pk>',UpdateAddress.as_view(),name="update"),
    path('deleteaddress/<int:pk>',DeleteAddress.as_view(),name="deleteadress"),
    path('payment',PaymentView.as_view(),name="payment"),
    path('myorder',MyOrder.as_view(),name='myorder'),


    #---------------------------- Owner --------------------------------

    path('dashaboard',Dashaboard.as_view(),name="dashaboard"),
    path('requestorder',RequestForOrder.as_view(),name="request_order"),
    path('aproveorder/<int:pk>',AproveOrder.as_view(),name="aproveorder"),
    path('additem',AddItem.as_view(),name='additem'),
    path('allitem',AllItem.as_view(),name = 'allitem'),
    path('allorder',AllOrder.as_view(),name = 'allorder'),
    path('deleteitem/<int:pk>',DeleteItem.as_view(),name = 'deleteitem'),
    path('addbrand',AddBrand.as_view(),name = 'addbrand'),
    path('addcategory',AddCategory.as_view(),name = "addcategory"),
    path('allbrand',AllBrand.as_view(),name = "allbrand"),
    path('allcategory',AllCategory.as_view(),name = "allcategory"),
    path('deletebrand/<int:pk>',DeleteBrand.as_view(),name = 'deletebrand'),
    path('deletecategory/<int:pk>',DeleteCategory.as_view(),name = 'deletecategory'),

]