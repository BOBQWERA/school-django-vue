import os
from urllib.parse import quote

from django.shortcuts import render
from django.http import FileResponse
from django.http import Http404

from school.settings import BASE_DIR
import function
# Create your views here.

def index(request):
    message = function._get_logined_message(request)
    message['tools'] = function._get_tools_message()
    return render(request,'tools/index.html',message)

def upload(request):
    message = function._get_logined_message(request)
    if not message['logined']:
        raise Http404('page not found')
    if request.method == 'POST':
        obj = request.FILES.get('file')
        password = request.POST.get('password')
        urlname = function._create_random_urlname()
        function._create_uploader(obj.name,urlname,password)
        with open(os.path.join(os.path.join(BASE_DIR,'files'),urlname),'wb') as f:
            for chunk in obj.chunks(chunk_size=1024):
                f.write(chunk)
        res = 'url: /tools/download/'+urlname+'\r\npassword: '
        if password:
            res+= password
        else:
            res+= 'none'
        response = FileResponse(res)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="url.txt"'
        return response
    return render(request,'tools/upload.html',message)

def download(request,urlname):
    file = function._get_file_by_urlname(urlname)
    if not file:
        raise Http404('file not found')
    if not file.password or request.method=='POST' and request.POST['password'] == file.password:
        content = open(os.path.join(os.path.join(BASE_DIR,'files'),file.urlname),'rb')
        response = FileResponse(content)
        response['Content-Type'] = 'application/octet-stream'
        print(file.name)
        response['Content-Disposition'] = f'attachment;filename="{quote(file.name)}"'
        return response
    else:
        return render(request,'tools/check.html',{'urlname':file.urlname})

def md5(request):
    message = function._get_logined_message(request)
    if request.method=='POST':
        message['result']=function._md5_result(request.POST.get('string'))
    return render(request,'tools/md5.html',message)

def base64(request):
    message = function._get_logined_message(request)
    if request.method == 'POST' and request.POST['string']:
        string = request.POST['string']
        if request.POST['direct']=='toB':
            message['result'] = function._string_to_base64(string)
        elif request.POST['direct'] == 'toV':
            message['result'] = function._base64_to_string(string)
    return render(request,'tools/base64.html',message)

def wordcet4(request):
    message = function._get_logined_message(request)
    return render(request,'tools/word.html',message)