from django.shortcuts import render
import requests, json
from django.conf import settings
from datetime import datetime
from base64 import b64encode
from .credentials import get_access_token, get_response, verify_response
from django.http import JsonResponse, HttpResponse
from .models import MpesaPayment, SuccessfulTransfer, UnsuccessfulTransfer
from .forms import PaymentForm
from django.views.decorators.csrf import csrf_exempt

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
    transactions = SuccessfulTransfer.all_transactions()

    return render(request, 'safaricom/mpesa.html',{
        'title':title,
        'form':payment_form,
        'transactions':transactions,
    })

def create_payment(request):
    f_name = request.POST.get('first_name')
    p_number = request.POST.get('phone_number')
    amount = request.POST.get('amount')
    new_payment = MpesaPayment(first_name=f_name, phone_number=p_number, amount=amount)
    new_payment.save()

    print(get_access_token(settings.CONSUMER_KEY,settings.CONSUMER_SECRET))
    # print(encryptInitiatorPassword(settings.INITIATOR_PASS, time_stamp))

    access_token = get_access_token(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    request = {
        "BusinessShortCode": settings.TILL_NO,
        "Password": (b64encode(f'{settings.TILL_NO}{settings.INITIATOR_PASS}{create_time()}'.encode('ascii'))).decode('ascii'),
        "Timestamp": create_time(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": p_number,
        "PartyB": settings.TILL_NO,
        "PhoneNumber": p_number,
        "CallBackURL": f"https://{request.get_host()}/safaricom/verify_payment/",
        "AccountReference": "NewPlan",
        "TransactionDesc": "Thank you"
    }
    response = get_response(api_url, request, headers)
    print (response.text)
    
    return JsonResponse({'success':'SUccess'})

@csrf_exempt
def verify_payment(request):    
    raw_data = request.body.decode('utf-8')
    data = json.loads(raw_data)
    result_code = data['Body']['stkCallback']['ResultCode']
    merchant_request_id = data['Body']['stkCallback']['MerchantRequestID']
    checkout_request_id = data['Body']['stkCallback']['CheckoutRequestID']
    # entry to database
    if result_code == 0:
        amount = data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        receipt_no = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        transaction_date = data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
        phone_number = data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
        success_transfer = SuccessfulTransfer(merchant_id=merchant_request_id, checkout_request_id=checkout_request_id, result_code=result_code, mpesa_receipt_no=receipt_no, amount=amount, transaction_date=transaction_date,phone_number=phone_number)
        success_transfer.save()
    else:
        description = data['Body']['stkCallback']['ResultDesc']
        fail_transfer = UnsuccessfulTransfer(merchant_id=merchant_request_id, checkout_request_id=checkout_request_id, result_code=result_code, result_description=description)
        fail_transfer.save()

    return HttpResponse(request.body.decode('utf-8'))