from django.db import models

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
    bitcoin=models.FloatField()
    bnb=models.FloatField()
    eth=models.FloatField()

    def __str__(self):
        return(str(self.id)+" BTC:"+str(self.bitcoin)+" BNB:"+str(self.bnb)+" ETH:"+str(self.eth))