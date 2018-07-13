from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LogoutView
from AWSEnroll.views import CustomLoginview

urlpatterns = [
    path('accounts/login/', CustomLoginview.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('AWSEnroll.urls')),
    url(r'^admin/', admin.site.urls, name='admin'),
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
