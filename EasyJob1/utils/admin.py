import sys
from django.contrib import admin

# Register your models here.
from utils import models

class AreaAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'cno')

class CitiesAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'pno')

class JobseekerAdmin(admin.ModelAdmin):
	list_display = ('emill','name', 'sex', 'loc','polistatus','birth','grad','phone')

class PositionAdmin(admin.ModelAdmin):
	list_display = ('compno','indus', 'name', 'grad','salary','loc','type','date')

class CompanyAdmin(admin.ModelAdmin):
	list_display = ('emill','phone','name','code', 'boss', 'reg_l','reg_d','state','loc','loccode')


#admin.site.register(models.Application)
admin.site.register(models.Areas,AreaAdmin)
admin.site.register(models.Cities, CitiesAdmin)
admin.site.register(models.Company,CompanyAdmin)
#admin.site.register(models.Industy)
#admin.site.register(models.Invitation)
#admin.site.register(models.Job_Intention)
admin.site.register(models.Jobseeker,JobseekerAdmin)
admin.site.register(models.Position,PositionAdmin)
admin.site.register(models.Provinces)
#admin.site.register(models.School)