from celery import shared_task
from .models import Order
from django.core.mail import send_mail






@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"Your Order id is : {order.id}"
    message = f"Dear {order.first_name} Your Order is Ready"
    mail_send = send_mail(subject , message , "admin@admin.com"  ,[order.email])
    return mail_send
    




