import os

from django.shortcuts import render
from django.http import Http404,HttpResponse,FileResponse

from django.conf import settings

from tools.views import download
# Create your views here.

def get_image(request,imgname):
    if imgname in os.listdir('files/image'):
        img = open('files/image/'+imgname,'rb')
    else:
        raise Http404('img not found')
    response = HttpResponse(content = img.read(),content_type = 'image/jpeg')
    return response

def get_file(request,filename):
    return download(request,filename)
    