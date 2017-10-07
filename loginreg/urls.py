from django.conf.urls import url
from . import views    

urlpatterns = [
	url(r'^$', views.index),
	url(r'^index$', views.index),
	url(r'^success$', views.success),
	url(r'^create_user$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
]	