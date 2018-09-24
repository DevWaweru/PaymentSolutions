from django.db import models

# Create your models here.
class PaypalTransaction(models.Model):
    first_name = models.CharField(max_length=50)
    order_id = models.CharField(max_length = 100)
    payer_id = models.CharField(max_length = 100)
    payment_id = models.CharField(max_length = 100)
    nonce = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.order_id}'
    
    class Meta:
        ordering = ('-id',)

    @classmethod
    def all_transactions(cls):
        transactions = PaypalTransaction.objects.all()
        return transactions