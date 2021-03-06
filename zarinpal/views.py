from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect ,render
from orders.models import Order, OrderItem
import requests
import json
from django.core.mail import EmailMessage
# from .tasks import payment_completed







MERCHANT = "7QRXP08Y-VA0D-R4T4-AOF3-FXYXRAFGGV5T"
ZP_API_REQUEST = "https://banktest.ir/gateway/zarinpal/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://banktest.ir/gateway/zarinpal/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://banktest.ir/gateway/zarinpal/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'https://mega-game.ir/zarinpal/verify/'


def send_request(request):
	global total_cost
	order_id = request.session.get('order_id')
	order = get_object_or_404(Order,id=order_id)
	total_cost = order.get_total_cost()
	total_cost = total_cost * 10 #Change Rial to Toman
	req_data = {
		"merchant_id": MERCHANT,
		"amount": total_cost,
		"callback_url": CallbackURL,
		"description": description,
		"metadata": {"mobile": mobile, "email": email}
	}
	req_header = {"accept": "application/json",
				  "content-type": "application/json'"}
	req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
		req_data), headers=req_header)
	authority = req.json()['data']['authority']
	if len(req.json()['errors']) == 0:
		return redirect(ZP_API_STARTPAY.format(authority=authority))
	else:
		e_code = req.json()['errors']['code']
		e_message = req.json()['errors']['message']
		return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request):
	order_id = request.session.get('order_id')
	order = get_object_or_404(Order,id=order_id)
	t_status = request.GET.get('Status')
	t_authority = request.GET['Authority']
	if request.GET.get('Status') == 'OK':
		req_header = {"accept": "application/json",
					  "content-type": "application/json'"}
		req_data = {
			"merchant_id": MERCHANT,
			"amount": total_cost,
			"authority": t_authority
		}
		req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
		if len(req.json()['errors']) == 0:
			t_status = req.json()['data']['code']
			if t_status == 100:
				order.paid = True
				order.save()
				if request.user.email:
					mail_subject = "ثبت سفارش "
				message = "مشتری گرامی سفارش شما ثبت شد و پس از بررسی، سفارش برای شما ارسال میشود"
				email = EmailMessage(
							mail_subject,
							message,
							to=[request.user.email]
				)
				email.send()
				return render(request,"zarinpal/success.html",{"id":str(req.json()['data']['ref_id'])})
			elif t_status == 101:
				return render(request,"zarinpal/submited.html",{"status":str(req.json()['data']['message'])})
			else:
				return render(request,"zarinpal/failed.html",{"status":str(req.json()['data']['message'])})
		else:
			return render(request,"zarinpal/error.html")
	else:
		return render(request,"zarinpal/cancel.html")
	   
