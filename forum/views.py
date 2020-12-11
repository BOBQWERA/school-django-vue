from django.shortcuts import render,redirect
from django.http import Http404
from django.utils.safestring import mark_safe

import function
# Create your views here.

def index(request):
    message = function._get_logined_message(request)
    message['sections'] = function._get_sections()
    return render(request,'forum/index.html',message)

def section(request,section):
    if not function._has_section_by_urlname(section):
        raise Http404('section not found')
    function._visit(request,section)
    message = function._get_logined_message(request)
    message.update(function._get_section_message(request,section))
    message['section_name'] = function._get_section_name_by_urlname(section)
    return render(request,'forum/section.html',message)


def write(request,section):
    message = function._get_logined_message(request)
    message['section_name'] = function._get_section_name_by_urlname(section)
    message['urlname'] = section
    return render(request,'forum/write.html',message)

def save(request,section):
    if not function._logined(request) or request.method !='POST':
        raise Http404('page not found')
    function._save_posting(request)
    message=function._get_logined_message(request)
    return redirect('../..',context=message)

def posting(request,section,pid):
    p = function._get_posting_by_pid(pid)
    if not p:
        raise Http404('posting not found')
    message = function._get_logined_message(request)
    message['posting'] = p[0]
    if 'username' in message.keys():
        message['selfposting'] = p[0].landlord.username == message['username']
    message['section_name'] = function._get_section_name_by_urlname(section)
    message['postingHtml'] = mark_safe(p[0].text)
    if request.method == 'POST':
        print(request.POST)
        function._posting_add_comment(request,p[0])
        return redirect('.',context=message)
    comments= function._handle_comments(function._get_comment(pid))
    for i in comments:
        i[1] = mark_safe(i[1])
    message['comments'] = comments
    return render(request,'forum/posting.html',message)

def del_comment(request,cid):
    function._delete_comment(cid)
    from_url = request.headers.get('Referer')
    return redirect(from_url)

def rep_comment(request,cid):
    function._report_comment(request,cid)
    from_url = request.headers.get('Referer')
    return redirect(from_url)

def pass_comment(request,cid):
    is_superuser = function._is_superuser(request)
    if not is_superuser:
        raise Http404('page not found')
    function._pass_comment(cid)
    from_url = request.headers.get('Referer')
    return redirect(from_url)