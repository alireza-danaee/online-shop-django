from django.shortcuts import redirect, render
from .forms import OrderCreateForm 
from .models import OrderItem
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse





def order_create(request):
    cart = Cart(request)
    user = request.user
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order , product=item['product'] , price=item['price'] , quantity=item['quantity'],user=user)
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id 
            return redirect(reverse('zarinpal:request'))
    else:
        form = OrderCreateForm()
    return render(request , 'orders/create_order.html' , {'form' : form , 'cart':cart})

    
