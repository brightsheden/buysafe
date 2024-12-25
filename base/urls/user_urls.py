from django.urls import path
from base.views import user_view as views


urlpatterns = [
path('profile/', views.profile,name='profile'),
path('balance/', views.userbalance,name='balance'),
path('editProfile/', views.editProfile, name='editProfile'),
path('withdrawals/', views.WithdrawalListCreateView.as_view(), name='withdrawal_list_create'),
path('submitwithdrawal/', views.submit_withdrawal),
path('mywithdrawals/', views.get_user_withdrawals ),
path('withdrawals/approve/<int:pk>/', views.ApproveWithdrawalView.as_view(), name='approve_withdrawal'),
path('wallets', views.getWallets),
path("manual_transaction", views.manual_transaction, name="manual_transaction"),


]


