from django import forms
from .models import Order



class OrderCreateForm(forms.ModelForm):

    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name','phone', 'email', 'address', 'postal_code', 'city' , 'state','description_user']

        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control',}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.Textarea(attrs={'class':'form-control'}),
            'postal_code':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'description_user':forms.Textarea(attrs={'class':'form-control','style':'height:60px'}),
        }
        