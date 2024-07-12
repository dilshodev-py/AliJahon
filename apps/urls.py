from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from apps.views import CategoryListView, CustomLoginView

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout')
]

