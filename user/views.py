from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404

import function
# Create your views here.

def login(request):
    message = function._get_logined_message(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if function._check_user(username,password):
            obj = redirect('index')
            obj.set_cookie('sessionid',function._make_sessionid(username,function._password_to_md5(password)))
            obj.set_cookie('username',username)
            obj.content = message
            return obj
    return render(request,'user/login.html',message)


def register(request):
    message = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        nickname = request.POST['nickname']
        repeat = request.POST['repeat']
        telephone = request.POST['telephone']
        email = request.POST['email']
        if not function._check_same_password(password,repeat):
            message['repeat_username']=True
        elif not function._new_username(username):
            message['repeat_failed']=True
        else:
            function._create_user(username,nickname,password,telephone,email)
            return redirect('login')
    else:
        message = {'blank':True}
    message.update(function._get_logined_message(request))
    return render(request,'user/register.html',message)

def exit(request):
    from_url = request.headers.get('Referer')
    response = redirect(from_url)
    response.delete_cookie('username')
    response.delete_cookie('sessionid')
    return response

def userspace(request,username):
    if not function._has_user(username):
        raise Http404('user not found')
    if function._self_space(request,username):
        message={'personal':True}
    else:
        message={'personal':False}
    message.update(function._get_logined_message(request))
    if request.method=='POST':
        fromUsername = message['username']
        say = request.POST['say']
        function._apply_add_friend(fromUsername,username,say)
    message.update(function._get_space_message(username))
    message['mastername']=function._get_nikename_by_username(username)
    message['masterusername']=username
    message['friend'] = '+friend'
    message['wait'] = bool(function._get_waiting(username,message['username']))
    message['isfriend'] = function._is_friend(username,message['username'])
    message['signed'] = not function._not_sign_this_day(function._get_user_by_username(username))
    if function._self_space(request,username):
        message['self'] = function._get_user_by_username(username)
        message['friends'] = function._get_friends_by_username(username)
        message['applys'] = function._get_applys_by_username(username)
        return render(request,'user/self_space.html',message)
    return render(request,'user/user_space.html',message)

# def friend(request,username):
#     fromUsername = function._logined(request)
#     function._apply_add_friend(fromUsername,username)
#     if function._self_space(request,username):
#         message={'personal':True}
#     else:
#         message={'personal':False}
#     message.update(function._get_logined_message(request))
#     message.update(function._get_space_message(username))
#     message['mastername']=function._get_nikename_by_username(username)
#     message['wait'] = True
#     return render(request,'user/user_space.html',message)

def add_friend(request,username,friend):
    function._add_friend(username,friend)
    return redirect(f'/user/{username}/')

def refuse(request,username,friend):
    function._refuse(username,friend)
    return redirect(f'/user/{username}')

def sign(request,username):
    function._sign(username)
    return redirect(f'/user/{username}')