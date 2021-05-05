from accounts.api import views
from django.conf.urls import url
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
  
urlpatterns = [
    # path('register', views.Register.as_view(), name='register'),
    path('validatePhone/', views.ValidatePhoneSendOTP.as_view()),
    path('validateotp/', views.ValidateOTP.as_view()),
	path('login/',views.ObtainAuthTokenView.as_view(), name='login'),
    path('properties', views.account_properties_view, name='properties'),
    path('properties/update', views.update_account_view, name='accountupdate'),
    path('profile', views.profile_properties_view, name='profile'),
    path('profile/update', views.update_profile_view, name='profileupdate'),
	path('register/', views.registration_view, name='register'),
    # path('instuctorregister/', views.InstructorRegister, name='instructorregister'),
    path('change_password/', views.ChangePasswordView.as_view(), name="change_password"),
    path('check_if_account_exists/',  views.does_account_exist_view, name="check_if_account_exists"),
    # path('rest_activate/<uidb64>/<token>/$', views.rest_activate,name='rest_activate'),
]