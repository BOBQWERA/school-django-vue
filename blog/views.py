from django.shortcuts import render,redirect
from django.http import Http404
from django.utils.safestring import mark_safe

import function
# Create your views here.

def index(request):
    message = {}
    message.update(function._get_logined_message(request))
    message.update(function._get_blog_message(request))
    return render(request,'blog/blog.html',message)

def write(request):
    message=function._get_space_message(request)
    message.update(function._get_logined_message(request))
    return render(request,'blog/write.html',message)

def save(request):
    if not function._logined(request) or request.method !='POST':
        raise Http404('page not found')
    function._save_article(request)
    message=function._get_logined_message(request)
    return redirect('..',context=message)

def article(request,aid):
    article = function._get_blog_by_id(aid)
    message={'article':article}
    message.update(function._get_logined_message(request))
    articleHtml = mark_safe(article.text)
    message['articleHtml'] = articleHtml
    if message.get('username'):
        message['have_not_like'] = not function._liked_blog(message['username'],aid)
    return render(request,'blog/article.html',message)
    
def all_blog(request):
    articles = function._get_blog()
    message = function._get_logined_message(request)
    message['articles'] = articles
    if articles:
        message['has_blog'] = True
    else:
        message['has_blog'] = False
    return render(request,'blog/all_articles.html',message)

def success(request,aid):
    is_superuser = function._is_superuser(request)
    if not is_superuser:
        raise Http404('page not found')
    function._pass_blog(aid)
    from_url = request.headers.get('Referer')
    return redirect(from_url)

def like(request,aid):
    function._like_blog(request,aid)
    form_url = request.headers.get('Referer')
    return redirect(form_url)

def report(request,aid):
    function._report_blog(request,aid)
    form_url = request.headers.get('Referer')
    return redirect(form_url)

def delete(request,aid):
    is_superuser = function._is_superuser(request)
    if not is_superuser:
        raise Http404('page not found')
    function._delete_blog(aid)
    from_url = request.headers.get('Referer')
    return redirect(from_url)