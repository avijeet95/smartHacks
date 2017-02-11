from django.contrib import admin
from trip.models import Trip, Job, Worker
# Register your models here.
class TripAdmin(admin.ModelAdmin):
	
	class Meta :
		model = Trip

class JobAdmin(admin.ModelAdmin):
	# list_display = ("uid","fname")
	class Meta :
		model = Job

class WorkerAdmin(admin.ModelAdmin):
	# list_display = ("uid","fname")
	class Meta :
		model = Worker
admin.site.register(Trip)
admin.site.register(Job)
admin.site.register(Worker)