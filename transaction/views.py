from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Account,Transaction_History
import random
from django.conf import settings
from django.core.mail import send_mail


def hi(request):
    return HttpResponse("hi")

def home(request):
    return render(request, 'home.html')
def deposit(request):
    if request.method=="POST":
        account_number=request.POST.get('account_number'," ")
        amount=request.POST.get('amount'," ")
        try:
            if float(amount)%500==0 or float(amount)%100==0:
                account = Account.objects.get(account_number=account_number)
                account.balance+=float(amount)
                account.save()
                messages.success(request,f"Successfully deposited {amount}")
                Transaction_History.objects.create(account=account,amount=amount,transaction_type='deposit')
            #messages.success(request,"object created Successfully")
                return redirect('deposit')
            else:
                messages.error(request,"Deposit allowed only in 100 or 500 only")
                return redirect('deposit')
        except Account.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect('deposit')
        except ValueError :
            messages.error(request,"Please Enter Numbers only")
            return redirect('deposit')
        
    return render(request,'deposit.html')
def withdrawl(request):# to get account number and amount 
    if request.method=="POST":
        account_number=request.POST.get('account_number')
        amount=request.POST.get('amount')
        try:
            account=Account.objects.get(account_number=account_number)
            if float(amount)>account.balance or float(amount)<500 or float(amount)%500!=0 or float(amount)%100!=0:
                messages.error(request,"Insufficient Amount")
                return redirect('withdrawl')
            else:
               return redirect('withdraw_amount',account_number=account_number,amount=amount)
        except Account.DoesNotExist:
            messages.error(request,"Invalid Credentials")
            return redirect('withdrawl')
        except ValueError:
            messages.error(request,"Please Enter Numbers only")
            return redirect('withdrawl')
    return render(request,'withdrawl.html')
def withdraw_amount(request,account_number,amount):# to confirm pin for that account number
    if request.method=='POST':
        account=Account.objects.get(account_number=account_number)
        pin=request.POST.get('pin')
        try:
            if  pin!=str(account.pin):
                messages.error(request,"Invalid Account number or Pin")
                return render(request,"pin.html")
            else:
                account.balance-=float(amount)
                account.save()
                Transaction_History.objects.create(account=account,amount=amount,transaction_type='withdrawl')
                messages.success(request,f"Successfully withdrawn {amount}")
                return redirect('withdrawl')

        except ValueError :
            messages.error(request,"Please Enter Numbers only")
            return redirect('withdraw_amount',account_number=account_number,amount=amount)
    return render(request,"pin.html")
def check_balance(request):
    if request.method=="POST":
        account_number=request.POST.get('account_number')
        pin=request.POST.get('pin')
        try:
            account=Account.objects.get(account_number=account_number)
            if pin!=str(account.pin):
                messages.error(request,"Invalid Account Number or Pin ")
                return redirect("check_balance")
            else:
                messages.success(request,f"Your current balance is {account.balance}")
                return redirect('check_balance')
        except Account.DoesNotExist:
            messages.error(request,'Invalid Credentials')
            return render(request,'balance.html')
        except ValueError :
            messages.error(request,"Please Enter Numbers only")
            return redirect('check_balance')
    return render(request,'balance.html')
def pin_generation(request):
    if request.method=='POST':
        account_number=request.POST.get('account_number')
        try:
            account=Account.objects.get(account_number=account_number)
            new_pin=random.randint(1000,9999)
            subject = 'New Pin'
            message = f" Your new pin is {new_pin}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [account.email]
            send_mail(subject, message, from_email, recipient_list)
            messages.info(request,"Your new pin has been sent to your Email.Kindly Check your Email.")
            return redirect('pin',new_pin=new_pin,account_number=account_number)
        except Account.DoesNotExist:
            messages.error(request,"Invalid Account Number")
            return render(request,'account.html')
    return render(request,'account.html')
def pin(request,new_pin,account_number):#to confirm pin 
    if request.method=='POST':
        pin=request.POST.get('pin')
        try:
            if pin!=str(new_pin):
                messages.error(request,"Invalid Pin")
            else:
        
                account=Account.objects.get(account_number=account_number)
                account.pin=pin
                account.save()
                messages.success(request,"Your new pin generated Successfully")
                return redirect('pin_generation')
        except ValueError :
            messages.error(request,"Please Enter Numbers only")
            return render(request,'pin.html')
    return render(request,'pin.html',{"new_pin":new_pin,"account_number":account_number})
def transaction_history(request):
    if request.method=="POST":
        account_number=request.POST.get('account_number')
        pin=request.POST.get('pin')
        try:
            account=Account.objects.get(account_number=account_number)
            transactions=Transaction_History.objects.filter(account__account_number=account_number).order_by('-date')[:5]
            if pin!=str(account.pin):
                messages.error(request,"Invalid Account Number or Pin ")
                return redirect('transaction_his')
            else:
                return render(request,'transaction_his.html',{"transactions":transactions})
        except Account.DoesNotExist:
            messages.error(request,"Invalid Credentials")
            return redirect('transaction_his')
        except ValueError:
            messages.error(request,"Please Enter Numbers only")
            return redirect('transaction_his')
    return render(request,'balance.html')
            










