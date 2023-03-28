from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import AccountSerializer,UserName_Serializer,TransactionSerializer
from .models import Account,User,Wallet, Transaction
import json
import requests, datetime
from django.utils import timezone

my_datetime = timezone.now()

# Create your views here.

# List all Users and merchant in db
@api_view(['GET'])
def accounts(request):
    if request.method == 'GET':
        accounts=Account.objects.all()
        serializer=AccountSerializer(accounts, many=True)
        print(AccountSerializer(accounts, many=True))
        return Response(serializer.data,status=status.HTTP_200_OK)


# For user log in authentication
@api_view(['POST'])    
def user_login(request):
    json_data = request.body
    #Check if posted data is correct Format/complete
    post_serializer=AccountSerializer(data=request.data)
    if post_serializer.is_valid():
        data = json.loads(json_data)
        data_email = data['email']
        data_password = data['password']
        #print(data)
        query_account=Account.objects.filter(email=data_email, password=data_password, merchant=False)
        if not query_account:
            #print("incorrect")
            return Response({"status" : "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            #print(query_account)
            id = query_account.values_list('id', flat=True).first()
            query_name=User.objects.filter(id=id)
            if query_name:
                name=query_name.values_list('name',flat=True).first()
                return Response({"id":id, "name":name, "status" : "success"}, status=status.HTTP_200_OK)
                #print(name)
            #print(type(id))
            #print(id)
            
    return Response({"status" : "incomplete"}, status=status.HTTP_424_FAILED_DEPENDENCY)


# For user sign up
@api_view(['POST'])  
def user_signup(request):
    json_data = request.body
    account=AccountSerializer(data=request.data)
    user=UserName_Serializer(data=request.data)
    if account.is_valid() and user.is_valid():
         account_instance=account.save()
         user_instance = User(id=account_instance, name=request.data.get("name"))
         user_instance.save()
         return Response({"status" : "created"}, status=status.HTTP_201_CREATED)
    return Response({"status" : "incomplete"}, status=status.HTTP_424_FAILED_DEPENDENCY)


@api_view(['POST'])
def user_wallet(request):
    bitcoin_sgd=3000
    bnb_sgd=400
    eth_sgd=2000
    response=requests.get('https://api.coingecko.com/api/v3/ping')
    if response.status_code == 200:
        response=requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=sgd')
        data = response.json()
        bitcoin_sgd= data['bitcoin']['sgd']
        bitcoin_sgd=round(bitcoin_sgd,2)

        response=requests.get('https://api.coingecko.com/api/v3/simple/price?ids=binancecoin&vs_currencies=sgd')
        data = response.json()
        bnb_sgd= data['binancecoin']['sgd']
        bnb_sgd=round(bnb_sgd,2)

        response=requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=sgd')
        data = response.json()
        eth_sgd= data['ethereum']['sgd']
        eth_sgd=round(eth_sgd,2)
    
    #print(bitcoin_sgd, bnb_sgd, eth_sgd)

    # query the wallet amounts
    query_wallet=Wallet.objects.filter(id=request.data.get("id"))
    if not query_wallet:
        return Response({"status" : "wallet doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
    bitcoin=query_wallet.values_list('BTC', flat=True).first()
    bnb=query_wallet.values_list('BNB', flat=True).first()
    eth=query_wallet.values_list('ETH', flat=True).first()

    #convert to sgd
    converted_bitcoin=sgd_conversion(bitcoin_sgd, bitcoin)
    converted_bnb=sgd_conversion(bnb_sgd, bnb)
    converted_eth=sgd_conversion(eth_sgd, eth)
 
    #print(bitcoin_sgd, bnb_sgd, eth_sgd)
    total_balance=round(converted_bitcoin+converted_bnb+converted_eth,2)
    data_to_return={
        "id": request.data.get("id"),
        "total_balance":str(total_balance),
        "wallets":[
        {
            "name":"Bitcoin",
            "crypto":"BTC",
            "amount": str(bitcoin),
            "converted_amount":str(converted_bitcoin),
            "rate":str(bitcoin_sgd)
        },
        {
            "name":"Binance Coin",
            "crypto":"BNB",
            "amount": str(bnb),
            "converted_amount":str(converted_bnb),
            "rate":str(bnb_sgd)
        },
        {
            "name":"Ethereum",
            "crypto":"ETH",
            "amount": str(eth),
            "converted_amount":str(converted_eth),
            "rate":str(eth_sgd)
        }
        ]
    }
    return Response(data_to_return,status=status.HTTP_200_OK)
    


# currency conversion - return up to 4 decimal place
def sgd_conversion(price, amount):
    return round(price*amount, 2)

@api_view(['POST'])
def send_crypto(request):
    transaction=TransactionSerializer(data=request.data)
    if transaction.is_valid():
        crypto_upper_case=transaction.data['crypto']
        crypto_upper_case=crypto_upper_case.upper()
        sender_wallet=Wallet.objects.filter(id=transaction.data['sender'])
        receiver_wallet=Wallet.objects.filter(id=transaction.data['receiver'])

        
        if sender_wallet and receiver_wallet:
            #print(sender_wallet)
            #print(receiver_wallet)
            sender_coin=sender_wallet.values_list(crypto_upper_case, flat=True).first()
            receiver_coin=receiver_wallet.values_list(crypto_upper_case, flat=True).first()

            if(transaction.data['amount']>sender_coin):
                return Response({"status":"not enough coin"}, status=status.HTTP_400_BAD_REQUEST)
            
            sender_coin=round(sender_coin-transaction.data['amount'],2)
            receiver_coin=round(receiver_coin+transaction.data['amount'],2)
            #print("sender")
            #print(sender_coin)

            sender_wallet.update(**{crypto_upper_case:sender_coin})
            receiver_wallet.update(**{crypto_upper_case:receiver_coin})

            date_time=my_datetime.astimezone(timezone.get_current_timezone())
            transaction_num=gen_transaction_id(transaction.data['sender'],transaction.data['receiver'],crypto_upper_case,transaction.data['amount'],date_time)
            transaction_instance = Transaction(
                sender=transaction.data['sender'], 
                receiver=transaction.data['receiver'],
                crypto=crypto_upper_case,
                amount=transaction.data['amount'],
                time=date_time,
                transaction_id=transaction_num
                )
            
            print(transaction_instance)
            #query_wallet=Wallet.objects.filter(id=request.data.get("id"))
            #sender_wallet=query_wallet.values_list('bitcoin', flat=True).first()
            #print(datetime.datetime.now())
            #print (datetime.datetime.now().date())
            #print (datetime.datetime.now().time())
            transaction_instance.save()
            return Response({"status":"success", "transaction_id":str(transaction_num)},status=status.HTTP_200_OK)
    return Response({"status":"fail"}, status=status.HTTP_400_BAD_REQUEST)

def gen_transaction_id(sender,receiver,type,amount,dtime):
   return_str=str(sender)+str(receiver)+str(type)+str(dtime)
   return_str=return_str.replace(':', '').replace('-', '').replace(' ', '')
   #print(return_str)
   return return_str

