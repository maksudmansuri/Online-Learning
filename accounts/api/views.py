from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate

from .serializers import RegistrationSerializer,AccountPropertiesSerializer,ProfilePropertiesSerializer,ChangePasswordSerializer

from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView)
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes

from rest_framework import status

from accounts.models import CustomUser,AdminHOD,Staffs,Students
from accounts.EmailBackEnd import EmailBackEnd

from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import (
	AllowAny,
	)
from rest_framework.authtoken.models import Token


# @api_view(['POST',])
# def StudentRegister(request):
	
# 	if request.method == "POST":
# 		serializer = StudentRegisterSerializer(data=request.data)
# 		data = {}
# 		if serializer.is_valid():
# 			user_obj = serializer.save(request)
# 			data['response'] = "successfully Registered a new user"
# 			data['email'] = user_obj.email
# 			data['username'] = user_obj.username
# 			token = Token.objects.get(user=user_obj).key
# 			data['token'] = token
# 		else:
# 			data = serializer.errors
# 		return Response(data) 

# @api_view(['POST',])
# def InstructorRegister(request):
	
# 	if request.method == "POST":
# 		serializer = InstructorRegisterSerializer(data=request.data)
# 		data = {}
# 		if serializer.is_valid():
# 			user_obj = serializer.save(request)
# 			data['response'] = "successfully Registered a new user"
# 			data['email'] = user_obj.email
# 			data['username'] = user_obj.username
# 			token = Token.objects.get(user=user_obj).key
# 			data['token'] = token
# 		else:
# 			data = serializer.errors
# 		return Response(data) 

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0').lower()
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data)

		serializer = RegistrationSerializer(data=request.data)
		
		if serializer.is_valid():
			account = serializer.save(request)
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

def validate_email(email):
	account = None
	try:
		account = CustomUser.objects.get(email=email)
	except CustomUser.DoesNotExist:
		return None
	if account != None:
		return email

def validate_username(username):
	account = None
	try:
		account = CustomUser.objects.get(username=username)
	except CustomUser.DoesNotExist:
		return None
	if account != None:
		return username


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def account_properties_view(request):
	try:
		account = request.user
	except CustomUser.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = AccountPropertiesSerializer(account)
		return Response(serializer.data)


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
	try:
		account = request.user
	except CustomUser.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	if request.method == 'PUT':
		serializer = AccountPropertiesSerializer(account,data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = "Account Updated Successfully"
			return Response(data=data)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def profile_properties_view(request):
	try:
		account = Students.objects.get(admin=request.user)
		print(account)
	except Students.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = ProfilePropertiesSerializer(account)
		return Response(serializer.data)
	

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_profile_view(request):
	try:
		account = Students.objects.get(admin=request.user)
	except Students.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	if request.method == 'PUT':
		serializer = ProfilePropertiesSerializer(account,data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = "Account Updated Successfully"
			return Response(data=data)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		account = EmailBackEnd.authenticate(request,username=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			if account.is_active == True:
				context['response'] = 'Successfully authenticated.'
				context['pk'] = account.pk
				context['email'] = email.lower()
				context['token'] = token.key
			else:
				context['response'] = 'Error'
				context['error_message'] = 'Check you email for activte account'
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)

@api_view(['GET', ])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):

	if request.method == 'GET':
		email = request.GET['email'].lower()
		data = {}
		try:
			account = CustomUser.objects.get(email=email)
			data['response'] = "Email Exists"
		except CustomUser.DoesNotExist:
			data['response'] = "Account does not exist"
		return Response(data)

class ChangePasswordView(UpdateAPIView):

	serializer_class = ChangePasswordSerializer
	model = CustomUser
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

			# confirm the new passwords match
			new_password = serializer.data.get("new_password")
			confirm_new_password = serializer.data.get("confirm_new_password")
			if new_password != confirm_new_password:
				return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

			# set_password also hashes the password that the user will get
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response({"response":"successfully changed password"}, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class StudentRegister(CreateAPIView):
# 	permission_classes = (AllowAny,)

# 	serializer_class = StudentRegisterSerializer

# 	queryset = CustomUser.objects.all()
    
# class InstructorRegister(CreateAPIView):
# 	permission_classes = (AllowAny,)

# 	serializer_class = InstructorRegisterSerializer
# 	queryset = CustomUser.objects.all()