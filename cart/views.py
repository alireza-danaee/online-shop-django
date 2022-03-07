from django.shortcuts import redirect, render ,get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from shop.models import Product
from coupons.forms import CouponApplyForm
# Create your views here.



@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart or update its quantity
    """
    cart = Cart(request)
    product = get_object_or_404(Product , id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product , quantity=cd['quantity'] , override_quantity=cd['override'])
        
        return redirect('cart:cart_detail')



@require_POST
def cart_remove(request , product_id):
    cart = Cart(request)
    product = get_object_or_404(Product , id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
        



def cart_detail(request):
    cart = Cart(request)
    form_apply_code = CouponApplyForm()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item['quantity'],
            'override':True
        })
    context = {
        'cart':cart,
        'form':form_apply_code,
    }
    return render(request , 'cart/cart_detail.html' , context)
