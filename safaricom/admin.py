from django.contrib import admin
from .models import MpesaPayment, SuccessfulTransfer, UnsuccessfulTransfer

# Register your models here.
admin.site.register(MpesaPayment)
admin.site.register(SuccessfulTransfer)
admin.site.register(UnsuccessfulTransfer)