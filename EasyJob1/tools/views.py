# coding:utf-8
from django.shortcuts import render
from utils import models
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
import MySQLdb
from django.http import JsonResponse
import time

# Create your views here.

def setSession(request):
    pno= request.GET['pno']
    cno= request.GET['cno']
    request.session['pno']=str(pno)
    request.session['cno'] =str(cno)
    data = {'status': 0, 'msg': 'true'}
    return JsonResponse(data)


def getdata(sql):
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
    index = cur.description
    result = []
    for res in cur.fetchall():
        row = []
        for i in range(len(index)):
            row.append(res[i])
        result.append(row)
    return result


def getdescription(sql):
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
    return cur.description


def getcity(request):
    pno = request.GET['procode']
    citys = models.Cities.objects.filter(pno=str(pno))
    data = serializers.serialize('json', citys)
    return HttpResponse(data, content_type='application/json')


def getarea(request):
    no = request.GET['cityno']
    areas = models.Areas.objects.filter(cno=str(no))
    data = serializers.serialize('json', areas)
    return HttpResponse(data, content_type='application/json')


def getsecondindustry(request):
    no = request.GET['code']
    second = models.Industy.objects.filter(pre=str(no))
    data = serializers.serialize('json', second)
    return HttpResponse(data, content_type='application/json')


# --------------------------------------------------------------------

dataset=getdata("SELECT c.`name` as cname,p.name as pname,p.salary,p.grad,a.`name` as area,p.date FROM utils_position p,utils_company c,utils_areas a WHERE p.compno=c.id AND p.loc=a.code ")
def get_position_page(request):
    global dataset
    n = request.GET["index"]
    index = int(n)
    if (index<len(dataset)/9) and (index>=1):
        temp=(index-1)*9
        data = dataset[temp:temp+9]
    elif index==1:
        data = dataset[0:9]
    else:
        temp=len(dataset)-(index-1)*9+1
        data = dataset[temp:len(dataset)]
    data = {'status': 0, 'msg': '请求成功', 'data': data}
    return JsonResponse(data)

def job_search(request):
    sql="SELECT c.`name` as cname,p.name as pname,p.salary,p.grad,a.`name` as area,p.date FROM utils_position p,utils_company c,utils_areas a WHERE p.compno=c.id AND p.loc=a.code "
    indus = str(request.GET["indus"])
    salary = str(request.GET["salary"])
    loc = str(request.GET["loc"])
    grad = int(request.GET["grad"])
    type = str(request.GET["type"])
    keyword = str(request.GET["keyword"])
    global dataset
    dataset=getdata(sql)
    if type!="请选择":
        #sql = "SELECT c.`name` as cname,p.name as pname,p.salary,p.grad,a.`name` as area,p.date FROM utils_position p,utils_company c,utils_areas a WHERE p.compno=c.id AND p.loc=a.code AND p.type='%s'"%type
        sql = sql + " AND p.type='%s'" %type
        dataset=getdata(sql)
    if indus !='-1':
        #sql = "SELECT c.`name` as cname,p.name as pname,p.salary,p.grad,a.`name` as area,p.date FROM utils_position p,utils_company c,utils_areas a WHERE p.compno=c.id AND p.loc=a.code AND p.indus='%s'"%str(indus)
        sql = sql + " AND p.indus='%s'" %str(indus)
        dataset=getdata(sql)
    if grad !=-1:
        #sql = "SELECT c.`name` as cname,p.name as pname,p.salary,p.grad,a.`name` as area,p.date FROM utils_position p,utils_company c,utils_areas a WHERE p.compno=c.id AND p.loc=a.code AND p.grad<='%d'"%grad
        sql = sql + " AND p.grad<='%d'" %grad
        dataset=getdata(sql)
    if keyword.strip() !="":
        #sql = "SELECT c.`name` as cname,p.name as pname,p.salary,p.grad,a.`name` as area,p.date FROM utils_position p,utils_company c,utils_areas a WHERE p.compno=c.id AND p.loc=a.code AND c.name LIKE '%s%%'"%keyword
       sql = sql + " AND p.name LIKE '%%%s%%'" % keyword
       dataset=getdata(sql)
    #if salary.strip() !="-1":
        #sql = "SELECT c.`name` as cname,p.name as pname,p.salary,p.grad,a.`name` as area,p.date FROM utils_position p,utils_company c,utils_areas a WHERE p.compno=c.id AND p.loc=a.code AND p.salary>=11000 AND p.salary<13000"
    if salary.strip() == "1":
       sql = sql +  " AND p.salary>0 AND p.salary<=3000"
       dataset=getdata(sql)
    if salary.strip() == "2":
       sql = sql +  " AND p.salary>3000 AND p.salary<=5000"
       dataset=getdata(sql)
    if salary.strip() == "3":
       sql = sql +  " AND p.salary>5000 AND p.salary<=7000"
       dataset=getdata(sql)
    if salary.strip() == "4":
       sql = sql +  " AND p.salary>7000 AND p.salary<=9000"
       dataset=getdata(sql)
    if salary.strip() == "5":
       sql = sql +  " AND p.salary>9000 AND p.salary<=11000"
       dataset=getdata(sql)
    if salary.strip() == "6":
       sql = sql +  " AND p.salary>11000 AND p.salary<=13000"
       dataset=getdata(sql)
    if salary.strip() == "7":
       sql = sql +  " AND p.salary>13000"
       dataset=getdata(sql)

    if loc.strip() !="-1":
        #sql = "SELECT c.`name` as cname,p.name as pname,p.salary,p.grad,a.`name` as area,p.date FROM utils_position p,utils_company c,utils_areas a WHERE p.compno=c.id AND p.loc=a.code AND a.name LIKE '%%%s%%'" %loc
        sql = sql +  " AND a.name LIKE '%%%s%%'" %loc
        dataset=getdata(sql)

    print("查询sql为：%s" %sql)

    if(len(dataset)>9):
        data=dataset[0:9]
    else:
        data=dataset
    if (len(dataset)/9)<1:
        data = {'count': len(dataset), 'len': 1, 'data': data}
    else:
        data = {'count':len(dataset), 'len': len(dataset)/9, 'data': data}
    return JsonResponse(data)

def get_firm_page(request):
    n = request.GET["index"]
    index = int(n)
    sql = "SELECT c.name,c.loc,COUNT(*),p.date FROM utils_position p,utils_company c WHERE c.id=p.compno GROUP BY p.compno"
    firmlist=getdata(sql)
    if (index*9<len(firmlist)) and (index>=1):
        temp=(index-1)*9
        data = firmlist[temp:temp+9]
    elif index==1:
        data = firmlist[0:9]
    else:
        temp=len(firmlist)-(index-1)*9+1
        data = firmlist[temp:len(firmlist)]
    data = {'status': 0, 'msg': '请求成功', 'data': data}
    return JsonResponse(data)


def get_job_page(request):
    n = request.GET["index"]
    index = int(n)
    sql="SELECT c.`name` as cname,p.name as pname,p.salary,p.grad,a.`name` as area,p.date FROM utils_position p,utils_company c,utils_areas a WHERE p.compno=c.id AND p.loc=a.code "
    position = getdata(sql)
    paginator = Paginator(position, 9)
    try:
        data = paginator.page(index)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    temp = serializers.serialize('json', data)
    return HttpResponse(temp, content_type='application/json')


def getdeliverpage(request):
    n = request.GET["index"]
    index = int(n)
    dataset = models.Application.objects.all()
    paginator = Paginator(dataset, 9)
    try:
        data = paginator.page(index)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    temp = serializers.serialize('json', data)
    return HttpResponse(temp, content_type='application/json')


# 生成简历pdf
def get_info():
    c = canvas.Canvas("media/info.pdf")
    c.drawString(-100, -100, "resume")
    c.drawString(10, 10, "name")
    c.drawString(20, 10, "name")
    c.drawString(30, 10, "name")
    c.drawString(40, 10, "name")
    c.drawString(50, 10, "name")
    c.drawString(60, 10, "name")
    c.drawString(10, 30, "XXX")
    c.drawString(20, 30, "XXX")
    c.drawString(30, 30, "XXX")
    c.drawString(40, 30, "XXX")
    c.drawString(50, 30, "XXX")
    c.drawString(60, 30, "XXX")
    c.showPage()
    c.save()





def info_download(request):
    get_info()
    # do something...
    def file_iterator(file_name, chunk_size=1024):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = "media/info1.pdf"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def toudi(request):
    pn = request.GET['pno']
    un = request.session.get('userID')
    if str(un).strip()!="":
        user=models.Jobseeker.objects.get(emill=str(un))
        data = {'pos_no': int(pn),
           'uno': int(user.id),
           'date': str(time.strftime('%Y-%m-%d',time.localtime(time.time()))),
            'state':0
           }
        models.Application.objects.create(**data)
        data = {'status': 0, 'msg': 'true'}
    else:
        data = {'status': 0, 'msg': 'false'}
    return JsonResponse(data)

def get_desc_position(request):
    n = request.GET["index"]
    index = int(n)
    cno = request.session.get('cno')
    firm = models.Company.objects.get(name=str(cno))
    sql = "SELECT p.name,p.salary,p.grad,a.name,p.date FROM utils_position p,utils_areas a WHERE a.code=p.loc AND p.compno=%d"%int(firm.id)
    positionlist=getdata(sql)
    if (index*9<len(positionlist)) and (index>=1):
        temp=(index-1)*9
        data = positionlist[temp:temp+9]
    elif index==1:
        data = positionlist[0:9]
    else:
        temp=len(positionlist)-(index-1)*9+1
        data = positionlist[temp:len(positionlist)]
    data = {'status': 0, 'msg': '请求成功', 'data': data}
    return JsonResponse(data)

