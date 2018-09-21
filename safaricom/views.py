from django.shortcuts import render
import requests
from django.conf import settings
from datetime import datetime
from base64 import b64encode
from .credentials import get_access_token, get_response, verify_response
from django.http import JsonResponse, HttpResponse
from .models import MpesaPayment
from .forms import PaymentForm

# Create your views here.
def create_time():
    # Create timestamp 
    leo = datetime.today()
    time_list = [leo.month, leo.day, leo.hour, leo.minute, leo.second]
    new_list = [f'{leo.year}']
    for time in time_list:
        if len(str(time)) == 1:
            new_list.append(f'0{time}')
        else:
            new_list.append(f'{time}')            
    time_stamp = ''.join(new_list)

    return time_stamp

def safaricom(request):
    title = 'Safaricom'
    payment_form = PaymentForm()
    print(dir(request.body))
    return render(request, 'safaricom/mpesa.html',{
        'title':title,
        'form':payment_form,
    })

def create_payment(request):
    f_name = request.POST.get('first_name')
    p_number = request.POST.get('phone_number')
    amount = request.POST.get('amount')
    print(request.POST)
    new_payment = MpesaPayment(first_name=f_name, phone_number=p_number, amount=amount)
    new_payment.save()

    print(get_access_token(settings.CONSUMER_KEY,settings.CONSUMER_SECRET))
    # print(encryptInitiatorPassword(settings.INITIATOR_PASS, time_stamp))

    access_token = get_access_token(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    request = {
        "BusinessShortCode": "174379",
        "Password": (b64encode(f'{174379}{settings.INITIATOR_PASS}{create_time()}'.encode('ascii'))).decode('ascii'),
        "Timestamp": create_time(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": p_number,
        "PartyB": "174379",
        "PhoneNumber": p_number,
        "CallBackURL": f"https://payments-solutions.herokuapp.com/safaricom/verify_payment/",
        "AccountReference": "NewPlan",
        "TransactionDesc": "Thank you"
    }
    response = get_response(api_url, request, headers)
    print (response.text)
    # print((b64encode(f'{174379}{settings.INITIATOR_PASS}{time_stamp}'.encode('ascii'))).decode('ascii'))
    # return redirect('verify_payment')
    return JsonResponse({'success':f'{response.text}'})

def verify_payment(request):
    # access_token = "Access-Token"
    # api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
    # headers = {"Authorization": f"Bearer {access_token}"}
    # request = { "BusinessShortCode": "174379" ,
    #         "Password": (b64encode(f'{174379}{settings.INITIATOR_PASS}{create_time()}'.encode('ascii'))).decode('ascii'),
    #         "Timestamp": create_time(),
    #         "CheckoutRequestID": "ws_CO_DMZ_79608579_20092018190450068"
    # }

    # response = verify_response(api_url, request, headers)

    # print (response.text)
    return JsonResponse(request.POST)