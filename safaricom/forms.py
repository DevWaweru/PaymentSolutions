from django import forms
from .models import MpesaPayment

class PaymentForm(forms.ModelForm):
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'placeholder': '254712345678'}))
    class Meta:
        model = MpesaPayment
        fields = '__all__'
        exclude = ['time']