from django.shortcuts import render
from django.views.generic import ListView,CreateView
from shop.models import Product 
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.







class ProductListAdmin(LoginRequiredMixin,ListView):
    queryset = Product.objects.all()
    template_name = 'registration/home.html'


class ProductCreate(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['name','slug','description','image','image2','image3','image4','price','status','pishnahad','category']
    template_name = 'registration/product_create_update.html'