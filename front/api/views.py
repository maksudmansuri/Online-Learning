from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.pagination import PageNumberPagination

from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status

from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView)
from rest_framework.response import Response

from accounts.models import CustomUser,AdminHOD,Staffs,Students
from front.models import Course,Course_Modules,Course_Session,CourseCategory,CourseSubCategory,viewed
from front.api.serializers import CourseDatailSerializer,CourseDetailUpdateSerializer,CourseDetailCreateSerializer,CourseModuleDatailSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication

from rest_framework.filters import SearchFilter,OrderingFilter

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# from rest_framework.permissions import (
# 	AllowAny,
# 	)

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_course_view(request,slug):
	try:
		crs = Course.objects.get(course_slug=slug)
	except Course.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = CourseDatailSerializer(crs)
		return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_course_view(request,slug):
	try:
		crs = Course.objects.get(course_slug=slug)
	except Course.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	if crs.teacher != Staffs.objects.get(admin=request.user):
		return Response({'response': 'you dont have permisssion to edit that'})

	if request.method == "PUT":
		serializer = CourseDetailUpdateSerializer(crs,data=request.data,partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			data['pk'] = crs.pk
			data['course_name'] = crs.course_name
			data['course_fee'] = crs.course_fee
			data['course_duration'] = crs.course_duration
			data['course_level'] = crs.course_level
			data['course_desc'] = crs.course_desc
			data['course_slug'] = crs.course_slug
			image_url = str(request.build_absolute_uri(crs.course_image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['course_image'] = image_url
			data['username'] = crs.teacher.admin.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_teacher_of_course(request, slug):
	try:
		crs = Course.objects.get(course_slug=slug)
	except Course.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if crs.teacher.admin != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_delete_course_view(request,slug):
	try:
		crs = Course.objects.get(course_slug=slug)
	except Course.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if crs.teacher != Staffs.objects.get(admin=request.user):
		return Response({'response': 'you dont have permisssion to Delete that'})

	if request.method == "DELETE":
		oparetion = crs.delete()
		data = {}
		if oparetion:
			data["success"] = "deleted Successful"
		else:
			data["failure"] = "delete failed"

		return Response(data=data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_course_view(request):

	if request.method == 'POST':

		data = request.data
		data['teacher'] = Staffs.objects.get(admin=request.user).pk
		data['course_category'] = CourseCategory.objects.get(id=1).pk
		data['course_subcategory'] = CourseSubCategory.objects.get(id=1).pk
		print(data)
		serializer = CourseDetailCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			course_detail = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = course_detail.pk
			data['course_name'] = course_detail.course_name
			data['course_desc'] = course_detail.course_desc
			data['course_slug'] = course_detail.course_slug
			data['course_duration'] = course_detail.course_duration
			data['course_level'] = course_detail.course_level
			data['course_fee'] = course_detail.course_fee
			image_url = str(request.build_absolute_uri(course_detail.course_image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['course_image'] = image_url
			data['username'] = course_detail.teacher.admin.username
			data['course_subcategory'] = course_detail.course_subcategory.subcategory
			data['course_category'] = course_detail.course_category.category
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET',])
# @permission_classes((IsAuthenticated,))
class ApiCourseListView(ListAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseDatailSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('course_name','course_fee','course_level','teacher__admin__username')

class ApiCourseModuleListView(generics.ListAPIView):
	queryset = Course_Modules.objects.all()
	serializer_class = CourseModuleDatailSerializer

	def get(self,request,*args,**kwargs):
		# try:
		crs_id = Course.objects.get(id=self.kwargs.get('id'))
		mdl = self.queryset.filter(course=crs_id)
		response_data = self.get_serializer(mdl,many=True)
		return Response(
			{
				"data" : response_data.data
			}
		)
		# except Course.DoesNotExist:
		# 	raise serializers.V ValidationError(_("Course Does not Exist"))
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	

