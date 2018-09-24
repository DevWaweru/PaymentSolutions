from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from paypalrestsdk import BillingPlan, BillingAgreement, configure
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
import braintree
from .models import PaypalTransaction

# configuring paypal
gateway = braintree.BraintreeGateway(access_token=settings.ACCESS_TOKEN)

def paypal(request):
    client_token=gateway.client_token.generate()
    title = 'PayPal'
    transactions = PaypalTransaction.all_transactions()

    return render(request, 'paypal/paypal.html', {
        'title':title,
        'token':client_token,
        'transactions':transactions,
    })

def paynow(request):
    f_name = request.POST.get('first_name')
    order_id = request.POST.get('orderID')
    payer_id = request.POST.get('payerID')
    payment_id = request.POST.get('paymentID')
    nonce = request.POST.get('nonce')
    amount = request.POST.get('amount')     
    
    result = gateway.transaction.sale({
        "amount" : amount,
        "merchant_account_id": "USD",
        "payment_method_nonce" : nonce,
        "order_id" : order_id,
        "descriptor": {
            "name": "abcdefghijkl*mnopqrstu", # 12 characters before the * and 9 after
        },
        "shipping": {
            "first_name": "Scruff",
            "last_name": "McGruff",
            # "company": "Braintree",
            "street_address": "1234 Main St.",
            "extended_address": "Suite 403",
            "locality": "Bartlett",
            "region": "IL",
            "postal_code": "60103",
            "country_code_alpha2": "US"
        },
        "options" : {
            "paypal" : {
                "custom_field" : 'custom_field',
                "description" : 'description'
            },
        }
    })

    if result.is_success:
        success = f"Success ID: {result.transaction.id}"
        new_transaction = PaypalTransaction(first_name=f_name, order_id=order_id, payer_id=payer_id, payment_id=payment_id, nonce=nonce, amount=amount)
        new_transaction.save()

        data = {'success': success}
    else:
        success = f'{result.message}'
        data = {'success':f'Failed {success}'}

    return JsonResponse(data)