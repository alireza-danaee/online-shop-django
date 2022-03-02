from django import forms





class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'کد تخفیف خود را وارد کنید' , 'style':'width:250px'}))

    