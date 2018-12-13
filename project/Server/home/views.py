from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django import forms
import django_excel as excel

from django.utils import timezone
from .models import Post
from .models import TrackList
from .models import BsubList
from .models import AsubList
from .models import User
from .models import Sheet1


import datetime
# Create your views here.

class UploadFileForm(forms.Form):
	file = forms.FileField()


def import_data(request):
	Sheet1.objects.all().delete()

	if request.method == "POST":
		form = UploadFileForm(request.POST,
							  request.FILES)

		if form.is_valid():


			request.FILES['file'].save_book_to_database(
				models=[Sheet1],
				initializers=[None],
				mapdicts=[{'년도': 'number',
						   '학기': 'dummy',
						   '학수번호':'dummy',
						   '교과목명': 'subject',
						   '이수구분': 'dummy',
			               '교직영역': 'dummy',
				           '선택영역': 'dummy',
						   '학점': 'dummy',
			               '평가방식': 'dummy',
						   '등급': 'dummy',
		                   '평점': 'dummy',
			               '개설학과코드': 'dummy'}]
			)
			return redirect('resultTrack')
		else:
			return HttpResponseBadRequest()
	else:
		form = UploadFileForm()
	return render(
		request,
		'home/upload_form.html',
		{
			'form': form,
			'title': 'Import excel data into database example',
			'header': 'Please upload sample-data.xls:'
		})


def handson_table(request):
	return excel.make_response_from_tables(
		[Sheet1], 'handsontable.html')

def post_list(request):
	return render(request, 'home/main.html')


def allTrack(request):
	tracklists = TrackList.objects.all()
	bsublists=BsubList.objects.all()
	asublists=AsubList.objects.all()

	posts = Post.objects.filter(published_date__lte=timezone.now())

	context= { 'posts' : posts , 'tracklists':tracklists, 'bsublists':bsublists,'asublists':asublists}
	return render(request,'home/allTrack.html',context)

def resultTrack(request):

	users=User.objects.all()
	usersubs=Sheet1.objects.all()
	tracklists = TrackList.objects.all()
	bsublists=BsubList.objects.all()
	asublists=AsubList.objects.all()

	usersubs.update(number = request.user.get_username())  # 일괄 update 요청

	context={'users':users,
			 'usersubs':usersubs,
			 'tracklists':tracklists,
			 'bsublists':bsublists,
			 'asublists':asublists,
			 }

	return render(request, 'home/resultTrack.html',context)



def test(request):
	return render(request,'home/test.html')

def notice(request):
	posts = Post.objects.all().order_by('-created_date') #날짜 역순
	context = {'posts':posts }
	return render(request,'home/notice.html',context)