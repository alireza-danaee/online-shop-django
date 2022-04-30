from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
import requests
import json
from zeep import Client
from orders.models import Order
# from .tasks import payment_completed

client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:7000/zarinpal/verify/'


def send_request(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    total_cost = order.get_total_cost()
    result = client.service.PaymentRequest(MERCHANT, total_cost, description, order.email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    if request.GET.get('Status') == 'OK':
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order,id=order_id)
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            order.paid = True
            order.save()
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
            
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
            
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
            
    else:
        return HttpResponse('Transaction failed or canceled by user')
       
