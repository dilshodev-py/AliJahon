from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from apps.views import CategoryListView, CustomLoginView, ProductListView, ProductDetailView

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('product/list', ProductListView.as_view(), name='product_list'),
    path('product/detail/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout')
]

