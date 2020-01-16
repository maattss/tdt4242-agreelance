from django import forms
from .models import Payment

class PaymentForm(forms.Form):
    cardnumber = forms.CharField(max_length=20, label="Card Number")
    expirymonth = forms.CharField(max_length=2, label="Expiry Month")
    expiryyear = forms.CharField(max_length=2, label="Expiry Year")
    cvc = forms.CharField(max_length=4, label="CVC")
