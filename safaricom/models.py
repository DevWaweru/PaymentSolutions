from django.db import models

# Create your models here.
class MpesaPayment(models.Model):
    first_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    amount = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.time}'
    
class SuccessfulTransfer(models.Model):
    merchant_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    result_code = models.IntegerField()
    amount = models.IntegerField()
    mpesa_receipt_no = models.CharField(max_length=20)
    transaction_date = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.mpesa_receipt_no
    
    class Meta:
        ordering=('-id',) 
    
    @classmethod
    def all_transactions(cls):
        transactions = SuccessfulTransfer.objects.all()
        return transactions

class UnsuccessfulTransfer(models.Model):
    merchant_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    result_code = models.IntegerField()
    result_description = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.result_code}'