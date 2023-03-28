from django.db import models
from django.utils import timezone


# Create your models here.
class Account(models.Model):
    #id is auto inserted by django as Primary Key value
    # total 4 column 
    id = models.AutoField(primary_key=True)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    merchant=models.BooleanField(default=False)
    
    def __str__(self):
        #return ("user_id : "+str(self.id)+"     | email : "+self.email+"     | pswd : "+self.password+"     | merchant : "+str(self.merchant))
        return (str(self.id)+" "+self.email+" "+self.password+" "+str(self.merchant))
    
class User(models.Model):
    id = models.OneToOneField(Account, primary_key=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)

    def __str__(self):
        return(str(self.id)+" "+self.name)
     
class Wallet(models.Model):
    id=models.OneToOneField(Account, primary_key=True, on_delete=models.CASCADE)
    BTC=models.FloatField()
    BNB=models.FloatField()
    ETH=models.FloatField()

    def __str__(self):
        return(str(self.id)+" BTC:"+str(self.BTC)+" BNB:"+str(self.BNB)+" ETH:"+str(self.ETH))
    
class Transaction(models.Model):
    sender=models.IntegerField()
    receiver=models.IntegerField()
    time=models.DateTimeField()
    crypto=models.CharField(max_length=50)
    amount=models.FloatField()
    transaction_id=models.CharField(max_length=100, default="null")

    def __str__(self):
        tz = timezone.get_current_timezone()
        local_time = timezone.localtime(self.time, tz)
        return(str(self.sender)+" to "+str(self.receiver)+" at "+local_time.strftime("%Y-%m-%d %H:%M:%S %Z")+" "+self.crypto+" amount : "+str(self.amount)+" transaction_id :"+str(self.transaction_id))
