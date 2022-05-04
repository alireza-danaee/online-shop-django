from django.db import models
from shop.models import Product
from django.contrib.auth import get_user_model
from extensions.utils import jalali_converter
# Create your models here.




class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments',verbose_name="محصول")
    user = models.ForeignKey(get_user_model() , on_delete=models.CASCADE,verbose_name="کاربر")
    text = models.TextField(verbose_name="متن نظر")
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False , verbose_name="فعال ")

    class Meta:
        ordering = ['created_on']
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.user)

    def j_created_on(self):
        return jalali_converter(self.created_on)

    j_created_on.short_description = 'زمان ارسال'

