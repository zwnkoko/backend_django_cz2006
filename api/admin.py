from django.contrib import admin
from .models import Account,User, Wallet
# Register your models here.

admin.site.register(Account)
admin.site.register(User)
admin.site.register(Wallet)