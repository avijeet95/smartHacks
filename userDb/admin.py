from django.contrib import admin
from userDb.models import Person
# Register your models here.
class PersonAdmin(admin.ModelAdmin):
	list_display = ("uid","fname")
	class Meta :
		model = Person

admin.site.register(Person,PersonAdmin)