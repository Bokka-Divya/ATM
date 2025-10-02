from django.urls import path
from . import views
urlpatterns=[
	path('hi',views.hi),
	path('',views.home,name='home'),
	path('deposit/',views.deposit,name='deposit'),
	path('withdrawl/',views.withdrawl,name='withdrawl'),
	path('withdraw_amount/<str:account_number>/<str:amount>',views.withdraw_amount,name='withdraw_amount'),
	path('check_balance/',views.check_balance,name='check_balance'),
	path('pin_generation/',views.pin_generation,name='pin_generation'),
	path('pin/<int:new_pin>/<str:account_number>/',views.pin,name='pin'),
	path('transaction_history/',views.transaction_history,name='transaction_his'),

]