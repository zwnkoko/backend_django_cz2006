from django.db import models

# Create your models here.
class Account(models.Model):
    #id is auto inserted by django as Primary Key value
    # total 4 column 
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    merchant=models.BooleanField(default=False)
    
    def __str__(self):
        #return ("user_id : "+str(self.id)+"     | email : "+self.email+"     | pswd : "+self.password+"     | merchant : "+str(self.merchant))
        return (str(self.id)+" "+self.email+" "+self.password+" "+str(self.merchant))