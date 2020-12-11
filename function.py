import hashlib
import datetime
import random
import re
import base64
from io import BytesIO

import requests
from urllib.request import urlopen
from django.core.files import File
from django.utils.safestring import mark_safe
from django.utils import timezone
from school.settings import MEDIA_ROOT

from user.models import User, Visited, Apply, Like, Report
from blog.models import Blog
from forum.models import Section, Posting, Comment
from tools.models import Files, Tools
from imagedata.models import Imagedata, IMAGE_TYPE_CHOICES
from examine.models import Examine

e_zonghe = Examine.objects.get(name='综合管理')
e_shenhe = Examine.objects.get(name='内容审核')
e_report = Examine.objects.get(name='举报审核')


def _add_friend(username, friend):
    user = User.objects.get(username=username)
    friend = User.objects.get(username=friend)
    user.friend.add(friend)
    user.friend_apply.remove(friend)


def _apply_add_friend(fromUsername, toUsername, say):
    # print(fromUsername,toUsername)
    from_user = User.objects.get(username=fromUsername)
    to_user = User.objects.get(username=toUsername)
    Apply.objects.create(from_user=from_user, to_user=to_user, say=say)


def _base64_to_string(base64String):
    return base64.b64decode(base64String).decode('utf8')


def _check_same_password(password, repeat):
    return password == repeat


def _check_user(username, password):
    user = User.objects.filter(username=username)
    if not user:
        return False
    user = user[0]
    return user.password == _password_to_md5(password)


def _check_blog(blog):
    blog.ex = e_report
    blog.save()


def _check_comment(comment):
    comment.ex = e_report
    comment.save()


def _create_fake_articles(num, username):
    user = User.objects.get(username=username)
    from faker import Faker
    fake = Faker(locale='zh-CN')
    for _ in range(num):
        para = random.randint(10, 200)
        text = ''
        for i in fake.paragraphs(nb=para):
            text += '<p>'+i+'</p>'
        Blog.objects.create(author=user, headline=fake.word(),
                            text=text, share=True, abstract=fake.word())


def _create_random_urlname(length=10, strSet=None):
    ranstr = ''
    if type(strSet) != str or len(strSet) < 10:
        strSet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    for _ in range(length):
        ranstr += random.choice(strSet)
    return ranstr


def _create_uploader(name, urlname, password):
    Files.objects.filter(up_time__lt=datetime.datetime.now() +
                         datetime.timedelta(days=-7)).delete()
    Files.objects.create(name=name, urlname=urlname, password=password)


def _create_user(username, nickname, password, telephone, email):
    User.objects.create(username=username, nickname=nickname,
                        password=_password_to_md5(password), telephone=telephone,
                        email=email, usertype='NU', ex=e_zonghe)
    return True


def _delete_blog(aid):
    Blog.objects.filter(id=aid).delete()


def _delete_comment(cid):
    Comment.objects.filter(id=cid).delete()


def _get_applys_by_username(username):
    user = User.objects.get(username=username)
    return user.to_user.all()


def _get_blog(username=False, shared=True, ex_name='综合管理'):
    if username:
        if shared:
            return Blog.objects.filter(author__username=username).filter(share=True).filter(ex__name=ex_name)
        else:
            return Blog.objects.filter(author__username=username).filter(ex__name=ex_name)
    else:
        if shared:
            return Blog.objects.filter(share=True).filter(ex__name=ex_name)
        else:
            return Blog.objects.all().filter(ex__name=ex_name)


def _get_blog_by_id(aid):
    blogs = Blog.objects.filter(id=aid)
    if not blogs:
        return False
    return blogs[0]


def _get_blog_message(request, shared=True):
    message = {'has_blog': False, 'more': False}
    articles = _get_blog(shared=shared)
    if articles:
        message['has_blog'] = True
    message['articles'] = articles[:20]
    if len(articles) > 20:
        message['more'] = True
    if _logined(request):
        personal_message = _get_space_message(_logined(request), False)
        message['personal_blog'] = personal_message['articles']
        message['not_has_personal_blog'] = not personal_message['has_blog']
    return message


def _get_cookie_from_request(request):
    if 'Cookie' not in request.headers:
        return {}
    cookie_string = request.headers['Cookie']
    cookie_dict = {}
    for cookie in cookie_string.split('; '):
        name, value = cookie.split('=')
        cookie_dict[name] = value
    return cookie_dict


def _get_comment(pid=None, ex_name='综合管理'):
    comment = Comment.objects.filter(ex__name=ex_name)
    if not pid:
        return comment
    else:
        return comment.filter(posting__id=pid)


def _get_comment_by_id(cid, ex_name='综合管理'):
    comment = Comment.objects.filter(id=cid).filter(ex__name=ex_name)
    if comment:
        return comment[0]
    return None


def _get_friends_by_username(username):
    return User.objects.get(username=username).friend.all()


def _get_file_by_urlname(urlname):
    file = Files.objects.filter(urlname=urlname)
    if not file:
        return False
    return file[0]


def _get_logined_message(request):
    message = {'logined': False}
    username = _logined(request)
    if username:
        message = {'logined': True, 'username': username}
        user = _get_user_by_username(username)
        if user.usertype == 'SU':
            message['SU'] = True
    print(message)
    return message


def _get_nikename_by_username(username):
    return User.objects.get(username=username).nickname


def _get_posting_by_pid(pid):
    return Posting.objects.filter(id=pid)


def _get_sections(allows='NU'):
    return Section.objects.filter(allow_groups=allows)


def _get_section_by_urlname(name):
    if _has_section_by_urlname(name):
        return Section.objects.get(urlname=name)
    return False


def _get_sections_name():
    sections = []
    for item in Section.objects.all():
        sections.append(item.name)
    return sections


def _get_space_message(username, shared=True):
    message = {'has_blog': False, 'articles': [], 'more': False}
    if _get_blog(username, shared=shared):
        message['has_blog'] = True
        articles = _get_blog(username, shared=shared)
        if len(articles) > 10:
            message['more'] = True
        message['articles'] = articles[:10]
    message['sections'] = _offten_visited_section(username)
    return message


def _get_section_message(request, urlname):
    message = {'has_posting': False, 'more': False}
    message['section'] = _get_section_by_urlname(urlname)
    message['sections'] = _get_sections()
    message['urlname'] = urlname
    postings = Posting.objects.filter(section__urlname=urlname)
    if postings:
        message['has_posting'] = True
    if len(postings) > 20:
        message['more'] = True
    message['postings'] = postings[:20]
    return message


def _get_section_name_by_urlname(urlname):
    if not Section.objects.filter(urlname=urlname):
        return False
    return Section.objects.get(urlname=urlname).name


def _get_section_by_urlname(urlname):
    if not Section.objects.filter(urlname=urlname):
        return False
    return Section.objects.get(urlname=urlname)


def _get_tools_message():
    return Tools.objects.all()


def _get_user_by_username(username):
    return User.objects.get(username=username)


def _get_visited_name(username):
    visits = Visited.objects.filter(user__username=username)
    name = []
    for i in visits:
        name.append([i.section.name, i.section.urlname])
    return name


def _get_waiting(fromUsername, toUsername):
    # print(fromUsername,toUsername)
    return User.objects.get(username=toUsername).friend_apply.filter(username=fromUsername)


def _handle_comments(comments):
    res_list = []
    for comment in comments:
        content = comment.content.replace('\n', '<br>')
        append_file = comment.append_file
        imgs = re.findall('\[image:(.*?)\]', content)
        random_str = _create_random_urlname(30)
        for i in imgs:
            content = content.replace('[image:'+i+']', random_str)
        content = content.split(random_str)
        cHtml = ''
        for i in range(len(content)):
            if i != 0:
                cHtml += f"<img src='/files/image/{imgs[i-1]}'>"
            cHtml += f"<p>{content[i]}</p>"
        res_list.append([comment, cHtml, append_file])
    return res_list


def _has_section_by_urlname(name):
    return Section.objects.filter(urlname=name)


def _has_user(username):
    return User.objects.filter(username=username)


def _is_friend(thisName, thatName):
    user1 = User.objects.get(username=thisName)
    user2 = User.objects.get(username=thatName)
    return user1 in user2.friend.all()


def _is_superuser(request):
    username = _logined(request)
    if not username:
        return False
    user = _get_user_by_username(username)
    if user.usertype != 'SU':
        return False
    return True


def _liked_blog(username, aid):
    user = _get_user_by_username(username)
    return user.like_set.filter(tp='B').filter(to_id=aid)


def _like_blog(request, aid):
    blog = _get_blog_by_id(aid)
    if not blog:
        return None
    username = _logined(request)
    if not username:
        return None
    user = _get_user_by_username(username)
    if _liked_blog(username, aid):
        return None
    Like.objects.create(user=user, tp='B', to_id=aid)
    blog.number_of_likes += 1
    blog.save()
    return True


def _logined(request):
    cookie = _get_cookie_from_request(request)
    if 'username' not in cookie.keys() or 'sessionid' not in cookie.keys():
        return False
    username = cookie['username']
    user = User.objects.filter(username=username)
    if not user:
        return False
    password = user[0].password
    if _make_sessionid(username, password) != cookie['sessionid']:
        return False
    return username


def _make_sessionid(username, password):
    return hashlib.md5((username+password).encode(encoding='utf8')).hexdigest()


def _md5_result(string):
    md5hash = hashlib.md5(string.encode('utf8'))
    return md5hash.hexdigest()


def _new_username(username):
    return not _has_user(username)


def _not_sign_this_day(user):
    now = datetime.datetime.now().date()
    return user.last_signed.date() != now


def _offten_visited_section(username):
    visits = _get_visited_name(username)
    visits = sorted(visits, key=lambda x: visits.count(x))[::-1]
    for i in visits[::-1]:
        if visits.count(i) > 1:
            visits.remove(i)
    return visits[:5]


def _pass_blog(aid):
    blog = _get_blog_by_id(aid)
    blog.ex = e_zonghe
    blog.save()


def _pass_comment(cid):
    comment = _get_comment_by_id(cid, ex_name='举报审核')
    if comment:
        comment.ex = e_zonghe
        comment.save()


def _password_to_md5(password):
    return hashlib.md5(password.encode(encoding='utf8')).hexdigest()[3:14]


def _posting_add_comment(request, posting):
    comment = request.POST['comment']
    _file = request.FILES.get('file') if request.FILES.get('file') else None
    if _file:
        urlname = _create_random_urlname()
        with open(MEDIA_ROOT+'/'+urlname, 'wb') as f:
            for chunk in _file.chunks(chunk_size=1024):
                f.write(chunk)
        _file = Files.objects.create(name=_file.name, urlname=urlname)
    user = User.objects.get(username=_logined(request))
    floor = posting.floor+1
    posting.floor += 1
    posting.save()
    imgs = re.findall('!\[(.*?)\]', comment)
    for img in imgs:
        if '.' not in img:
            continue
        imgtp = img.split('.')[-1]
        if (imgtp, '.'+imgtp) not in IMAGE_TYPE_CHOICES:
            continue
        imgdata = requests.get(img)
        origin_name = img.split('/')[-1]
        imgname = _create_random_urlname()
        comment = comment.replace('!['+img+']', f'[image:{imgname}]')
        if imgdata.ok:
            r = urlopen(img)
            io = BytesIO(r.read())
            i = Imagedata.objects.create(
                name=imgname, tp=imgtp, origin_name=origin_name)
            i.image.save(imgname, File(io))
    Comment.objects.create(publisher=user, posting=posting,
                           content=comment, floor=floor, append_file=_file, ex=e_zonghe)


def _refuse(username, friend):
    user = User.objects.get(username=username)
    friend = User.objects.get(username=friend)
    user.friend_apply.remove(friend)


def _reported_blog(username, aid):
    user = _get_user_by_username(username)
    return user.report_set.filter(tp='B').filter(to_id=aid)


def _report_blog(request, aid):
    blog = _get_blog_by_id(aid)
    if not blog:
        return None
    username = _logined(request)
    if not username:
        return None
    user = _get_user_by_username(username)
    reported = _reported_blog(username, aid)
    if reported:
        rep = reported[0]
        rep.num += 1
        rep.save()
    else:
        Report.objects.create(user=user, tp='B', to_id=aid)
    if len(Report.objects.filter(tp='B').filter(to_id=aid)) >= 1:
        _check_blog(blog)
    return True


def _reported_comment(username, cid):
    user = _get_user_by_username(username)
    return user.report_set.filter(tp='C').filter(to_id=cid)


def _report_comment(request, cid):
    comment = _get_comment_by_id(cid)
    if not comment:
        return None
    username = _logined(request)
    if not username:
        return None
    user = _get_user_by_username(username)
    reported = _reported_comment(username, cid)
    if reported:
        rep = reported[0]
        rep.num += 1
        rep.save()
    else:
        Report.objects.create(user=user, tp='C', to_id=cid)
    if len(Report.objects.filter(tp='C').filter(to_id=cid)) >= 1:
        _check_comment(comment)
    return True


def _save_article(request):
    author = _logined(request)
    headline = request.POST['headline']
    text = mark_safe(request.POST['editor'])
    share = ('share' in request.POST)
    if 'abstract' in request.POST:
        abstract = request.POST['abstract']
    else:
        abstract = '暂无简介'
    Blog.objects.create(author=User.objects.get(username=author), headline=headline,
                        text=text, share=share,
                        abstract=abstract, ex=e_shenhe)


def _save_posting(request):
    landlord = User.objects.get(username=_logined(request))
    headline = request.POST['headline']
    text = mark_safe(request.POST['editor'])
    section = _get_section_by_urlname(request.POST['urlname'])
    Posting.objects.create(
        landlord=landlord, headline=headline, text=text, section=section, ex=e_zonghe)


def _self_space(request, username):
    cookie = _get_cookie_from_request(request)
    if 'username' not in cookie.keys() or not _logined(request):
        return False
    return cookie['username'] == username


def _sign(username):
    user = User.objects.get(username=username)
    if _not_sign_this_day(user):
        user.score += 3
        user.last_signed = timezone.now()
        user.save()


def _string_to_base64(string):
    return base64.b64encode(string.encode('utf8')).decode('utf8')


def _visit(request, section):
    section = _get_section_by_urlname(section)
    username = _logined(request)
    if not username:
        return None
    user = User.objects.get(username=username)
    Visited.objects.create(user=user, section=section)
