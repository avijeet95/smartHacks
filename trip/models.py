from django.db import models
from userDb.models import Person
# Create your models here.

class Trip(models.Model):
	tid = models.IntegerField(default=0)
	uid = models.CharField(max_length=50,null=True)
	lon1=models.CharField(max_length=50,null=True)
	lat1=models.CharField(max_length=50,null=True)
	lon2=models.CharField(max_length=50,null=True)
	lat2=models.CharField(max_length=50,null=True)
	budget = models.IntegerField(default = 0)
	weight = models.IntegerField(default = 1)
	desc = models.CharField(max_length=200)

	def __unicode__(self):
		return self.uid

class Job(models.Model):
	wid = models.ForeignKey(Person,on_delete=models.CASCADE,related_name="workId")
	tid = models.ForeignKey(Trip,on_delete=models.CASCADE)
	uid = models.ForeignKey(Person,on_delete = models.CASCADE,related_name="userId")
	amt = models.IntegerField(default = 0)

class Worker(models.Model):
	uid = models.CharField(max_length=15)
	source=models.CharField(max_length=50,null=True)
	destination = models.CharField(max_length=50, null = True)
