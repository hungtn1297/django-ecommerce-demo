from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('collection/', views.collection, name='collection'),
    path('shoes/', views.shoes, name='shoes'),
    path('racing_boots/', views.racing_boots, name='racing_boots'),
    path('search/', views.search, name='search'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('ajax/add_to_cart', views.add_to_cart, name='ajax/add_to_cart'),
    path('payment/', views.payment, name='payment'),
    path('payment/success', views.payment_success, name='payment_success'),
    path('order', views.order, name='order'),
    path('logout', views.logout, name='logout')
]
