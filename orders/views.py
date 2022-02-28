from django.shortcuts import render
from .forms import OrderCreateForm 
from .models import OrderItem
from cart.cart import Cart
from .tasks import order_created
# Create your views here.





def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order , product=item['product'] , price=item['price'] , quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            return render(request , 'orders/created_order.html', {'order':order})

    else:
        form = OrderCreateForm()
    return render(request , 'orders/create_order.html' , {'form' : form , 'cart':cart})

    
