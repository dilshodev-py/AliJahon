import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, DetailView
import django.contrib.auth.password_validation as validators

from apps.forms import OrderForm
from apps.models import Category, Product, User


class CategoryListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/trade/home-page.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['categories'] = Category.objects.all()
        return data


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/trade/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        cat_slug = self.request.GET.get("category")
        query = super().get_queryset()
        if cat_slug:
            query = query.filter(category__slug=cat_slug)
        return query

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        return data


class ProductDetailView(DetailView, FormView):
    form_class = OrderForm
    model = Product
    template_name = 'apps/trade/product-detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.save()
        return render(self.request, 'apps/trade/product-order.html', {'form': form})


class CustomLoginView(TemplateView):
    template_name = 'apps/auth/login.html'

    def post(self, request, *args, **kwargs):
        phone_number = re.sub(r'\D', '', request.POST.get('phone_number'))
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            # is_ = validators.validate_password(request.POST['PASSWORD'])

            user = User.objects.create_user(phone_number=phone_number, password=request.POST['password'])
            login(request, user)
            return redirect('home')
        else:
            user = authenticate(request, username=user.phone_number, password=request.POST['password'])
            if user:
                login(request, user)
                return redirect('home')

            else:
                context = {
                    "messages_error": ["Invalid password"]
                }
                return render(request, template_name='apps/auth/login.html', context=context)
