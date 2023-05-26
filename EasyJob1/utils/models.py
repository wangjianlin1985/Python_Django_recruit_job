#coding:utf-8
from __future__ import unicode_literals
from django.db import models

#---------公司
class Company(models.Model):
    id = models.AutoField(primary_key=True)  #Company编号
    name = models.CharField(max_length=50)   #公司名称
    code = models.CharField(max_length=50,null=True)  #社会信用代码
    boss = models.CharField(max_length=50,null=True)  #法定代表人
    reg_l = models.CharField(max_length=50,null=True)   #登记机关
    reg_d = models.DateField()   #成立日期
    state = models.CharField(max_length=20)   #登记状态：存续（在营、开业、在册）
    loc =  models.CharField(max_length=50,null=True)   #公司地址
    loccode = models.IntegerField()  #市区编号
    phone = models.CharField(max_length=50,null=True)   #公司电话
    emill = models.EmailField()   #公司邮箱
    def __str__(self):
       return self.name


# --------求职者信息表
class Jobseeker(models.Model):

    id = models.AutoField(primary_key=True)  #Jobseeker编号
    name = models.CharField(max_length=50)   #姓名
    sex = models.CharField(max_length=20)   #性别
    loc = models.CharField(max_length=50)   #籍贯
    polistatus = models.CharField(max_length=20)  # 政治面貌
    birth = models.DateField()   #年龄
    grad = models.IntegerField(default=0)  #
    phone = models.CharField(max_length=50)  #电话
    emill = models.EmailField()   #邮箱
    text = models.TextField()   #个人评价
    def __str__(self):
       return self.name

# --------学校信息表
class School(models.Model):
    id = models.AutoField(primary_key=True)  #School编号
    name = models.CharField(max_length=50)   #学校名称
    loc = models.CharField(max_length=50)     #所在市编号
    def __str__(self):
       return self.name

#-------------学历表
class Xueli(models.Model):
    id = models.AutoField(primary_key=True)  # 编号
    first = models.DateField()   #入学时间
    end = models.DateField()   #毕业时间
    sno = models.IntegerField(default=0)
    type = models.IntegerField(default=0)   #学历:博士/硕士/本科/大专/中专/高中
    uid = models.IntegerField(default=0)
    def __str__(self):
       return self.id


#----------一级行业分类信息表
class Industy(models.Model):
    id = models.AutoField(primary_key=True)  # First_Industy编号
    code = models.CharField(max_length=50)   #一级代码
    name = models.CharField(max_length=50)   #一级名称
    pre = models.CharField(max_length=50)
    def __str__(self):
       return u'%s %s %s'% self.code,self.name,self.pre

#---------职位信息表：
class Position(models.Model):
    id = models.AutoField(primary_key=True)  # Position编号
    compno = models.IntegerField(default=0)
    indus = models.CharField(max_length=20)  #行业编号
    name = models.CharField(max_length=50)  # 职位名称
    grad = models.IntegerField(default=0)   # 最低学历要求
    salary = models.IntegerField(default=0)  # 薪资
    desc = models.TextField()  # 职位描述
    loc = models.CharField(max_length=50) # 工作详细地点
    type = models.CharField(max_length=50) # 工作性质:实习/全职/兼职
    date = models.DateField() #发布日期
    def __str__(self):
       return self.name

#---------职位申请表
class Application(models.Model):
    id = models.AutoField(primary_key=True)  # Application编号
    pos_no = models.IntegerField(default=0)
    uno = models.IntegerField(default=0)
    date= models.DateField() #:申请日期
    state = models.BooleanField() #处理状态：企业待处理/企业通知面试
    def __str__(self):
       return self.date

# ---------职位邀请请表
class Invitation(models.Model):
    id = models.AutoField(primary_key=True)  # Invitation编号
    pos_no = models.IntegerField(default=0)
    uno = models.IntegerField(default=0)
    date = models.DateField()  #:申请日期
    state = models.BooleanField() # 处理状态：企业确认/拒绝
    def __str__(self):
        return self.user_id
# ---------省表
class Provinces(models.Model):
    id = models.AutoField(primary_key=True,default=0)  # Provinces编号
    code = models.IntegerField(default=0)  # 省代码
    name = models.CharField(max_length=50)    # 名称
    def __str__(self):
        return self.name

# ---------市表
class Cities(models.Model):
    id = models.AutoField(primary_key=True,default=0)  # Cities编号
    code = models.IntegerField(default=0)  # 市代码
    name = models.CharField(max_length=50)  #  名称
    pno=models.IntegerField(default=0)
    def __str__(self):
        return self.name

# ---------县区表
class Areas(models.Model):
    id = models.AutoField(primary_key=True,default=0)
    code = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    cno = models.IntegerField(default=0)
    def __str__(self):
        return self.name

# ---------求职意向表
class Job_Intention(models.Model):
    id = models.AutoField(primary_key=True)  # 编号
    type = models.CharField(max_length=20)   #期望工作类型
    salary = models.IntegerField(default=0)  #期望薪资
    loc = models.IntegerField(default=0)
    industryno = models.IntegerField(default=0) #行业编号
    uno = models.IntegerField(default=0) #用户编号
    def __str__(self):
        return self.positionid

# ---------宣讲会信息表
class Careertalk(models.Model):
    id = models.AutoField(primary_key=True)  # 编号
    name = models.IntegerField()  #公司编号
    citycode = models.CharField(max_length=128)  # 市区编号
    loc = models.CharField(max_length=128)   #地点
    desc = models.TextField()  # 描述
    date = models.DateField() #日期
    def __str__(self):
       return u'%s %s %s'% self.loc,self.desc,self.date

# --------用户信息表
class Login(models.Model):
    id = models.AutoField(primary_key=True)   #user编号
    username = models.CharField(max_length=50)   #用户名
    password = models.CharField(max_length=50)   #密码
    type = models.IntegerField(default=0)      #用户类型 0求职者 1企业
    state = models.BooleanField(default=False)  # false ：表示未激活 ture：标识激活
    def __unicode__(self):
       return self.username

class sysinfo(models.Model):
    id = models.AutoField(primary_key=True)  #编号
    userid = models.IntegerField()  #用户编号
    key = models.CharField(max_length=20)   #键
    value = models.CharField(max_length=50) #值
    def __unicode__(self):
       return self.key