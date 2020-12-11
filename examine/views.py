from django.shortcuts import render
from django.utils.safestring import mark_safe

import function
# Create your views here.

def index(request):
    message = function._get_logined_message(request)
    message['articles'] = function._get_blog(username=False,shared=False,ex_name='内容审核')
    message['report_blogs'] = function._get_blog(username=False,shared=False,ex_name='举报审核')
    comments = function._handle_comments(function._get_comment(ex_name='举报审核'))
    for i in comments:
        i[1] = mark_safe(i[1])
    message['comments'] = comments
    return render(request,'examine/index.html',message)