
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.conf import settings
from . import forms
from .models import Payment
from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse
# Create your views here.


def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request,'make_payment.html',{'payment':payment,'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = forms.PaymentForm()
    return render(request,'initiate_payment.html',{'payment_form':payment_form})

def verify_payment(request:HttpRequest,ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment,ref=ref)
    verified = payment.verfied_payment()
    if verified:
        messages.success(request,"Verification successfull")
    else:
        messages.error(request,"Verification failed")
    return redirect('initiate-payment')


