from django.urls import path
from . import views

urlpatterns = [
    path('all_accounts/', views.accounts),
    path('login/user/', views.user_login),
    path('signup/user/', views.user_signup),
    path('wallet/user/', views.user_wallet ),
    path('send/', views.send_crypto),
    path('transaction/hist/', views.transaction_hist),
]