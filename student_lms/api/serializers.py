from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
	ValidationError,
	EmailField,
)
from front.models import Course,Course_Modules,Course_Session,CourseCategory,CourseSubCategory
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from accounts.utils import generate_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
import os
from django.core.files.storage import default_storage,FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_COURSENAME_LENGTH = 5
MIN_COURSEDECS_LENGTH = 50
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError

from front.utils import is_image_size_valid

class CourseDatailSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_staffs')
    course_image 	 = serializers.SerializerMethodField('validate_course_image_url')

    class Meta: 
        model = Course 
        fields = ['course_name','course_fee','course_duration','course_level','course_slug','username','course_image',]

    def get_username_from_staffs(self,Course):
        username = Course.teacher.admin.username
        return username

    def validate_course_image_url(self, Course):
        course_image = Course.course_image
        new_url = course_image.url
        if "?" in new_url:
            new_url = course_image.url[:course_image.url.rfind("?")]
        return new_url


class CourseDetailUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Course
		fields = ['course_name','course_fee','course_duration','course_level','course_desc','course_image']

	def validate(self, crs):
		try:
			course_name = crs['course_name']
			if len(course_name) < MIN_COURSENAME_LENGTH:
				raise serializers.ValidationError({"response": "Enter a course_name longer than " + str(MIN_COURSENAME_LENGTH) + " characters."})
			
			course_desc = crs['course_desc']
			if len(course_desc) < MIN_COURSEDECS_LENGTH:
				raise serializers.ValidationError({"response": "Enter a course_desc longer than " + str(MIN_COURSEDECS_LENGTH) + " characters."})
			
			course_image = crs['course_image']
			url = os.path.join(settings.TEMP , str(course_image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in course_image.chunks():
					destination.write(chunk)
				destination.close()

			# Check image size
			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
				os.remove(url)
				raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			# if not is_image_aspect_ratio_valid(url):
			# 	os.remove(url)
			# 	raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
		except KeyError:
			pass
		return crs


class CourseDetailCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Course
		fields = ['course_name','course_fee','course_duration','course_level','course_desc','teacher','course_image','course_category','course_subcategory']

	def save(self):
		
		try:
			course_image = self.validated_data['course_image']
			course_name = self.validated_data['course_name']
			if len(course_name) < MIN_COURSENAME_LENGTH:
				raise serializers.ValidationError({"response": "Enter a course_name longer than " + str(MIN_COURSENAME_LENGTH) + " characters."})
			
			course_desc = self.validated_data['course_desc']
			if len(course_desc) < MIN_COURSEDECS_LENGTH:
				raise serializers.ValidationError({"response": "Enter a course_desc longer than " + str(MIN_COURSEDECS_LENGTH) + " characters."})
			
			course_detail = Course(
								teacher=self.validated_data['teacher'],
								course_name=course_name,
								course_desc=course_desc,
								course_image=course_image,
                                course_fee=self.validated_data['course_fee'],
                                course_duration=self.validated_data['course_duration'],
                                course_level=self.validated_data['course_level'],
								# course_slug=self.validated_data['course_slug'],
								course_subcategory=self.validated_data['course_subcategory'],
								course_category=self.validated_data['course_category'],
								is_appiled = True,
								)

			url = os.path.join(settings.TEMP , str(course_image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in course_image.chunks():
					destination.write(chunk)
				destination.close()

			# Check image size
			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
				os.remove(url)
				raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			# if not is_image_aspect_ratio_valid(url):
			# 	os.remove(url)
			# 	raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
			course_detail.save()
			return course_detail
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a course_name, some content, and an image."})

