from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from app.views import retrieve_path
from app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, url, include
from django.views.static import directory_index



urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^log/(?P<path>.*)$','app.views.retrieve_path', {
            'document_root': '/var/log/remote/',}),    )


