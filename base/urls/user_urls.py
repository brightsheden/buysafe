from django.urls import path
from base.views import user_view as views


urlpatterns = [
path('profile/', views.profile,name='profile'),
path('balance/', views.userbalance,name='balance'),
path('editProfile/', views.editProfile, name='editProfile'),

]

