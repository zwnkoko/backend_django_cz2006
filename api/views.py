from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import AccountSerializer,UserSerializer,UserName_Serializer
from .models import Account,User
import json
import requests

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
            id = query_account.values_list('id', flat=True)[0]
            query_name=User.objects.filter(id=id)
            if query_name:
                name=query_name.values_list('name',flat=True)[0]
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


@api_view(['GET'])
def user_wallet(request):
    response=requests.get('https://api.coingecko.com/api/v3/ping')
    print(response.status_code)
    users=User.objects.all()
    serializer=UserSerializer(users, many=True)
    print(UserSerializer(accounts, many=True))
    return Response(serializer.data,status=status.HTTP_200_OK)
    