from rest_framework import serializers
from .models import Account, User, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['id', 'email', 'password', 'merchant']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'name']


class UserName_Serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields=['sender', 'receiver', 'crypto', 'amount']
