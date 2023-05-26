# coding:utf-8
from django.shortcuts import render, render_to_response
# Create your views here.
from utils import models
from random import Random
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import re
from django.conf import settings as django_settings

# ---------------------------Utils-------------------------------------
import MySQLdb


class mydb:
    result = []
    def __init__(self):
        pass
    def execsql(self, sql):
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='website',
            charset='utf8',
        )
        cur = conn.cursor()
        cur.execute(sql)
        self.result = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return self.result

class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)


token_confirm = Token(django_settings.SECRET_KEY)  # 定义为全局变量


# index页面
def index(request):
    request.session['userID'] = ''
    request.session['type'] = ''
    request.session['Islogin'] = 'false'
    return render(request, 'index.html')  # 渲染index页面


# 邮箱验证
def active_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = models.Login.objects.filter(username=username)
        for user in users:
            user.delete()
        return HttpResponse(u'对不起，验证链接已经过期，请重新<a href=\"' + unicode(django_settings.DOMAIN) + u'/login\">注册</a>')
    try:
        user = models.Login.objects.get(username=username)
    except models.Login.DoesNotExist:
        return HttpResponse(u"对不起，您所验证的用户不存在，请重新注册")
    user.state = True
    user.save()
    message = u'验证成功，请进行<a href=\"' + unicode(django_settings.DOMAIN) + u'/login\">登录</a>操作'
    return HttpResponse(message)


# 找回密码
def findpw(request):
    return render(request, 'findpw.html')

# 修改密码
def changepw(request):
    return render(request, 'changepw.html')

# 注销
def loginout(request):
    type = request.session.get('type')
    request.session['userID'] = ''
    request.session['Islogin'] = 'false'
    if type == 'job':
        return render(request, 'jobs_home.html', {'flag': 'false'})
    else:
        return render(request, 'index.html')


# 登陆
def login(request):
    request.session['userID'] = ''
    request.session['type'] = ''
    request.session['Islogin'] = 'false'
    name = request.POST['username']
    pw = request.POST['password']
    type = request.POST['options']
    if str(type) == 'hr':  # 1企业  0:求职者
        hr = models.Login.objects.get(username=name, password=pw, type=1)
        if hr:
            request.session['userID'] = name
            request.session['type'] = 'hr'
            request.session['Islogin'] = 'true'
          #  firm=models.Company.objects.get(emill=name)
          #  sql="SELECT j.name FROM utils_application a,utils_jobseeker j,utils_position p,utils_company c WHERE a.pos_no=p.id AND a.uno=j.id AND p.compno=c.id AND p.compno=%d"%firm.id
           # db = mydb()
           # msg = db.execsql(sql)
            indus = models.Industy.objects.filter(pre='-1').values()
            proset = models.Provinces.objects.values()

            #查询公司发布的职位
            sql = "select utils_position.name as name,utils_position.date as date,utils_company.name,utils_position.salary,utils_position.type,utils_position.id  from utils_position,utils_company where utils_position.compno=utils_company.id and utils_company.emill='%s'" %name
            db = mydb()
            positions = db.execsql(sql)

            #查询公司信息
            company = models.Company.objects.filter(emill=name)[0]

            #用户投递记录
            sql = "select u.name as uname,p.name as pname,a.date as adate,a.id,a.state from utils_company c,utils_application a,utils_position p,utils_jobseeker u where  a.pos_no=p.id and a.uno=u.id and p.compno=c.id and c.emill='%s'" %name
            posintents = db.execsql(sql)

            return render(request, 'hr_home.html', {'positions': positions,
                                                    'posintents': posintents,
                                                    'company': company,
                                                    'indusrylist': indus,
                                                    'provincelist': proset})
        else:
            response = HttpResponseRedirect('/home')
            return response
    else:
        job = models.Login.objects.filter(username=name, password=pw, type=0)
        if job:
            request.session['userID'] = name
            print('登录中设置session: userID=%s' %name)
            print('查看是否设置成功userID=%s'% request.session.get('userID'))
            request.session['type'] = 'job'
            request.session['Islogin'] = 'true'
            return render(request, 'jobs_home.html')
        else:
            response = HttpResponseRedirect('/home')
            return response


# ---------------------------JOB-------------------------------------

# 求职者主页面
def job_home(request):
    var = request.session.get('Islogin')
   # msg=models.Invitation.objects.values()
    return render(request, 'jobs_home.html', {'flag': var})


# 求职者注册页面
def job_reg(request):
    name = request.POST['name']
    sex = request.POST.getlist("sex")
    birth = request.POST['date']
    loc = request.POST['loc']
    phone = request.POST['phone']
    emill = request.POST['emill']
    polistatus= request.POST['polistatus'] #政治面貌
    text = request.POST['text'] #个人评价
    pw = request.POST['pw1']
    job = {'name': str(name),
           'sex': str(sex[0]),
           'loc': str(loc),
           'birth': str(birth),
           'grad': 0,
           'phone': str(phone),
           'emill': str(emill),
           'polistatus':str(polistatus),
           'text': str(text)
           }
    login = {
        'username': str(emill),
        'password': str(pw),
        'type': 0,  # 1企业  0:求职者
    }
    models.Jobseeker.objects.create(**job)
    flag2 = models.Login.objects.create(**login)
    flag2.state = False
    flag2.save()
    global token_confirm
    token = token_confirm.generate_validate_token(name)
    message = "\n".join([u'{0},欢迎加入EeasyJob在线招聘网站'.format(name), u'请访问该链接，完成用户验证:',
                         '/'.join([django_settings.DOMAIN, 'activate', token])])
    send_mail(u'注册用户验证信息', message, 'PhoneListener052@126.com', [emill, ], fail_silently=False)
    return HttpResponse(u"请登录到注册邮箱中验证用户，有效期为1个小时")


# 职位检索
def job_search(request):
    var = request.session.get('Islogin')
    indus = models.Industy.objects.filter(pre='-1').values()
    proset = models.Provinces.objects.values()
    sql = "SELECT c.`name` as cname,p.name as pname,p.salary,p.grad,a.`name` as area,p.date FROM utils_position p,utils_company c,utils_areas a WHERE p.compno=c.id AND p.loc=a.code "
    db = mydb()
    position = db.execsql(sql)
    paginator = Paginator(position, 9)
    data = position[0:9]
    return render(request, 'job_search.html', {
        'flag': var,
        'pagecount': paginator.num_pages,
        'current': 1,
        'indusrylist': indus,
        'provincelist': proset,
        'postions': data,
        'count': len(position)})


# 职位详情
def job_desc_position(request):

    var = request.session.get('Islogin')
    pno = request.session.get('pno')
    cno = request.session.get('cno')
    firm = models.Company.objects.filter(name=str(cno))
    posi = models.Position.objects.filter(name=str(pno))
    grad = ['博士','硕士','本科','专科','高中','其他']
    if firm:
        firm = firm[0]
    if posi:
        posi = posi[0]
        grad = grad[posi.grad-1]
        loc = posi.loc
        area = models.Areas.objects.filter(code=loc)
        if area is not None:
            area = area[0].name

    return render(request, 'desc_position.html', {
        'flag': var,
        'firm': firm,
        'position': posi,
        'grad': grad,
        'area': area
    })


# 公司详情
def job_desc_firm(request):
    var = request.session.get('Islogin')
    cno = request.session.get('cno')
    firm = models.Company.objects.get(name=str(cno))
    sql = "SELECT p.name,p.salary,p.grad,a.name,p.date FROM utils_position p,utils_areas a WHERE a.code=p.loc AND p.compno=%d" % int(
        firm.id)
    db = mydb()
    posi = db.execsql(sql)
    paginator = Paginator(posi, 9)
    data = posi[0:9]
    return render(request, 'desc_firm.html', {
        'pagecount': paginator.num_pages,
        'current': 1,
        'count': len(posi),
        'flag': var,
        'firm': firm,
        'position': data,
    })


# 宣讲会
def job_xjh(request):
    var = request.session.get('Islogin')
    proset = models.Provinces.objects.values()
    ctset = models.Careertalk.objects.all()
    return render(request, 'careertalk.html', {'flag': var, 'ctset': ctset, 'provincelist': proset})


# 公司
def job_firm(request):
    var = request.session.get('Islogin')
    proset = models.Provinces.objects.values()
    sql = "SELECT c.name,c.loc,COUNT(*),p.date FROM utils_position p,utils_company c WHERE c.id=p.compno GROUP BY p.compno"
    db = mydb()
    dataset = db.execsql(sql)
    paginator = Paginator(dataset, 9)
    data = dataset[0:9]
    return render(request, 'firmlist.html',
                  {'flag': var, 'pagecount': paginator.num_pages, 'current': 1, 'dataset': data,
                   'provincelist': proset})


# 投递记录
def job_deliver(request):
    var = request.session.get('Islogin')
    un = request.session.get('userID')
    if str(un).strip() == "":
        return render(request, 'message.html', {'flag': var, 'title': "提示!", "text": "请先登录！"})
    else:
        user = models.Jobseeker.objects.get(emill=str(un))
        sql = "SELECT c.name,p.name,a.date,area.name,a.state,a.id FROM utils_application a,utils_company c,utils_position p,utils_areas area where p.id=a.pos_no AND p.loc=area.code AND c.id=p.compno AND a.uno=%d" % int(
            user.id)
        db = mydb()
        dataset = db.execsql(sql)
        return render(request, 'delivercord.html', {'flag': var, 'dataset': dataset})


#企业用户删除投递
def job_del_deliver2(request):
    name = request.session.get('userID')
    id = int(request.GET.get("id"))
    models.Application.objects.get(id=id).delete()

    indus = models.Industy.objects.filter(pre='-1').values()
    proset = models.Provinces.objects.values()

    # 查询公司发布的职位
    sql = "select utils_position.name as name,utils_position.date as date from utils_position,utils_company where utils_position.compno=utils_company.id and utils_company.emill='%s'" % name
    db = mydb()
    positions = db.execsql(sql)

    # 查询公司信息

    company = models.Company.objects.filter(emill=name)[0]

    # 用户投递记录
    sql = "select u.name as uname,p.name as pname,a.date as adate,a.id,a.state from utils_company c,utils_application a,utils_position p,utils_jobseeker u where  a.pos_no=p.id and a.uno=u.id and p.compno=c.id and c.emill='%s'" % name
    posintents = db.execsql(sql)

    return render(request, 'hr_home.html', {'positions': positions,
                                            'posintents': posintents,
                                            'company': company,
                                            'indusrylist': indus,
                                            'provincelist': proset})


# 取消投递
def job_del_deliver(request):
    id = int(request.GET.get("id"))
    models.Application.objects.get(id=id).delete()
    var = request.session.get('Islogin')
    un = request.session.get('userID')
    if str(un).strip() == "":
        return render(request, 'message.html', {'flag': var, 'title': "提示!", "text": "请先登录！"})
    user = models.Jobseeker.objects.get(emill=str(un))
    sql = "SELECT c.name,p.name,a.date,area.name,a.state,a.id FROM utils_application a,utils_company c,utils_position p,utils_areas area where p.id=a.pos_no AND p.loc=area.code AND c.id=p.compno AND a.uno=%d" % int(
        user.id)
    db = mydb()
    dataset = db.execsql(sql)
    return render(request, 'delivercord.html', {'flag': var, 'dataset': dataset})


# 个人简历
def job_intro(request):
    user = request.session.get('userID')
    indus = models.Industy.objects.filter(pre='-1').values()
    proset = models.Provinces.objects.values()
    obj = models.Jobseeker.objects.get(emill=str(user))
    if obj:
        pass
    else:
        obj = models.Jobseeker()
        obj.name = "test"
    return render(request, 'introfrom.html', {'information': obj,
                                              'indusrylist': indus,
                                              'provincelist': proset,
                                              })


# ----------------------HR------------------------------------------

# 企业主页
def hr_home(request):
    indus = models.Industy.objects.filter(pre='-1').values()
    proset = models.Provinces.objects.values()
    return render(request, 'hr_home.html',{'indusrylist': indus,
        'provincelist': proset})


# 企业发布宣讲会
def hr_pub_xjh(request):
    date = request.POST['date']
    loc = request.POST['loc']
    desc = request.POST['desc']

    data = {'name': 1,
            'loc': str(loc),
            'desc': str(desc),
            'date': str(date),
            }
    models.Careertalk.objects.create(**data)
    return HttpResponse(u"发布成功！")


# 企业发布职位
def hr_pub_position(request):
    indus = request.GET['indus']
    name = request.GET['positionname']
    salary = request.GET['salary']
    type = request.GET['type']
    loc = request.GET['loc']
    grad = request.GET['grad']
    desc = request.GET['desc']
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    user = request.session.get('userID')
    firm=models.Company.objects.get(emill=str(user))
    print grad[0]
    data = {'compno': firm.id,
            #'indus': str(indus[0]),
            'indus': str(indus),
            'name': str(name),
            'grad': grad,
            'salary': int(salary),
            'desc': str(desc),
            #'loc': str(loc[0]),
            'loc': str(loc),
            #'type': str(type[0]),
            'type': str(type),
            'date': str(date),
            }
    models.Position.objects.create(**data)
    return HttpResponse(u"发布成功！")

# 企业删除职位
def hr_del_position(request):
    id = int(request.GET.get("id"))
    applictions = models.Application.objects.filter(pos_no=id)
    if len(applictions) > 0:
        return HttpResponse(u"该职位已经有人投递简历，删除失败！")
    else:
        models.Position.objects.get(id=id).delete()
        return HttpResponse(u"删除成功，请返回刷新网页看效果！")


# 企业注册
def hr_reg(request):
    name = request.POST['name']
    code = request.POST['code']
    boss = request.POST['boss']
    reg_l = request.POST['reg_l']
    reg_d = request.POST['reg_d']
    loc = request.POST['loc']
    phone = request.POST['phone']
    emill = request.POST['emill']
    pw = request.POST['pw1']
    firm = {'name': str(name),
            'code': str(code),
            'boss': str(boss),
            'reg_l': str(reg_l),
            'reg_d': str(reg_d),
            'state': str('在营'),
            'loc': str(loc),
            'loccode':'510108',  #这里默认是成都成华区，管理员可以后台去更新公司所在城市区域代码
            'phone': str(phone),
            'emill': str(emill)
            }
    login = {
        'username': str(emill),
        'password': str(pw),
        'type': 1,  # 1企业  0:求职者
    }

    models.Company.objects.create(**firm)
    flag2 = models.Login.objects.create(**login)
    flag2.state = False
    flag2.save()
    global token_confirm
    token = token_confirm.generate_validate_token(name)
    message = "\n".join([u'{0},欢迎加入EeasyJob在线招聘网站'.format(name), u'请访问该链接，完成用户验证:',
                         '/'.join([django_settings.DOMAIN, 'activate', token])])
    send_mail(u'注册用户验证信息', message, 'PhoneListener052@126.com', [emill, ], fail_silently=False)
    return HttpResponse(u"请登录到注册邮箱中验证用户，有效期为1个小时")


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

from django.http import JsonResponse
def action_findpw(request):
    emill = request.GET["emill"]
    try:
         user = models.Login.objects.get(username=str(emill))
         pw = random_str(8)
         user.password = pw
         user.save()
         message = u'\n尊敬的用户:您好！您的密码找回成功:' + pw
         send_mail(u'找回密码', message, 'PhoneListener052@126.com', [emill, ], fail_silently=False)
         data = {'status': 0, 'msg': 'true'}
    except Exception:
         data = {'status': 0, 'msg': 'false'}
    return JsonResponse(data)

def yaoqing(request):
    try:
         id = int(request.GET.get("id"))

         application = models.Application.objects.get(id=id)
         pid = int(application.pos_no)
         uid = int(application.uno)

         position = models.Position.objects.get(id=pid)
         cno = int(position.compno)

         company = models.Company.objects.get(id=cno)
         seeker = models.Jobseeker.objects.get(id=uid)

         print('begin开始邀请')
         message = u'\n尊敬的用户:您好！:我是' + company.name + '的HR，感谢你投递我公司职位' + position.name + '，现邀请您面试。地点：' + company.loc
         print(message)
         print(seeker.emill)
         send_mail(u'面试邀请', message, 'PhoneListener052@126.com', [seeker.emill, ], fail_silently=False)

         application.state = 1
         application.save()

         data = {'status': 0, 'msg': 'true'}
    except Exception:
         print('sorry邀请邮件发送失败')
         data = {'status': 0, 'msg': 'false'}
    return JsonResponse(data)