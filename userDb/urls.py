from django.conf.urls import include, url,static
urlpatterns=[
	url(r'^$','userDb.views.login',name='login'),
	url(r'^fetch/$','userDb.views.fetchUser',name ='fetchUser')
]
