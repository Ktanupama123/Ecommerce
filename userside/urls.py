from django.urls import path
from . import views
urlpatterns = [
    path('addproduct/',views.add_product,name='addproduct'),
    path('signup/',views.signupview,name='signup'),
    path('login/',views.signinview,name='login'),
    path('',views.productlist,name='productlist'),
    path('signout/', views.signoutview, name='signout'),
    path('delete/<int:id>', views.product_delete, name='delete'),
    path('edit/<int:id>/', views.product_edit, name='edit'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
]
