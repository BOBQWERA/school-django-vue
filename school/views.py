from django.shortcuts import render
from django.http import HttpResponse

import function
def index(request):
    message = function._get_logined_message(request)
    return render(request,'index.html',message)

def robots(request):
    return HttpResponse("User-Agent: *\nDisallow: *",content_type="text/plain")