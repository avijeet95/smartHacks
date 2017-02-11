from django.db import models

# Create your models here.
class Person(models.Model):
	uid = models.IntegerField(default=0)
	fname=models.CharField(max_length=50,null=False,blank=False)
	lname=models.CharField(max_length=55,null=False,blank=False)
	email=models.EmailField(null=True,blank=True)
	gender=models.CharField(max_length=10,null=False,blank=False)
	address = models.CharField(max_length=200, null=False, blank= False)
	aadhar=models.CharField(max_length=10,null=False,blank=False)
	credit = models.IntegerField(default=0)
	isWorker = models.BooleanField(default=False, blank = True)

	def __unicode__(self):
		return self.fname

