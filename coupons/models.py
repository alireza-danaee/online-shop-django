from django.db import models
from django.core.validators import MinValueValidator , MaxValueValidator
# Create your models here.



class Coupons(models.Model):
    code = models.CharField(verbose_name="کد تخفیف" , max_length=100)
    valid_from = models.DateTimeField(verbose_name="از زمان :")
    valid_to = models.DateTimeField(verbose_name="تا زمان :")
    discount = models.IntegerField(verbose_name="مقدار تخفیف" , validators=[MinValueValidator(0) , MaxValueValidator(100)])
    active = models.BooleanField(verbose_name= "فعال بودن کد")


    class Meta:
        verbose_name = "کوپن"
        verbose_name_plural = "کوپن ها"



    def __str__(self):
        return self.code
