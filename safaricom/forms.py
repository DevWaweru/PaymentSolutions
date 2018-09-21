from django import forms
from .models import MpesaPayment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = MpesaPayment
        fields = '__all__'
        exclude = ['time']