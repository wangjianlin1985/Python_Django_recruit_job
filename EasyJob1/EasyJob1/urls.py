"""EasyJob1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from utils import views as uviews
from tools import views as tviews

urlpatterns = [

    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', uviews.active_user, name='active_user'),
    url(r'^admin/', admin.site.urls),
    url(r'^home$', uviews.job_home, name='job_home'),
    url(r'^index$', uviews.index, name='index'),
    url(r'^login$', uviews.login),
    url(r'^regfirm$', uviews.hr_reg),
    url(r'^regjob$', uviews.job_reg),
    url(r'^findpw$', uviews.findpw),
    url(r'^loginout$', uviews.loginout),
    url(r'^jobsearch$', uviews.job_search),
    url(r'^careertalk$', uviews.job_xjh),
    url(r'^firmlist$', uviews.job_firm),
    url(r'^deliver$', uviews.job_deliver),
    url(r'^deliver_delete$', uviews.job_del_deliver),
    url(r'^deliver_delete2$', uviews.job_del_deliver2),
    url(r'^introform$', uviews.job_intro),
    url(r'^pubcareertalk$', uviews.hr_pub_xjh),
    url(r'^pubposition$', uviews.hr_pub_position),
    url(r'^delposition$', uviews.hr_del_position),
    url(r'^getcity$', tviews.getcity, name='getcity'),
    url(r'^getarea$', tviews.getarea, name='gesarea'),
    url(r'^getsecondindustry$', tviews.getsecondindustry, name='gesarea'),
    url(r'^queryposition$', tviews.get_position_page, name='queryposition'),
    url(r'^getfirmpage$', tviews.get_firm_page),
    url(r'^getpositionpage$', tviews.get_position_page),
    url(r'^infodownload$', tviews.info_download),
    url(r'^findpw$', uviews.findpw),
    url(r'^job_search_update$', tviews.job_search),
    url(r'^desc_position$', uviews.job_desc_position),
    url(r'^desc_firm$', uviews.job_desc_firm),
    url(r'^setSession$', tviews.setSession),
    url(r'^toudi$', tviews.toudi),
    url(r'^get_desc_position$', tviews.get_desc_position),
    url(r'^changepw$', uviews.changepw),
    url(r'^action_findpw$',uviews.action_findpw),
    url(r'^yaoqing$',uviews.yaoqing),
]
