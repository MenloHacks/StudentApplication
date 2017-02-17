"""menlohacks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from application.views import CustomRegistrationView, redirecting_login, \
    ResendEmail, is_active, ApplicationReviewView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('application.urls', namespace="application")),
    url(r'^accounts/login/', redirecting_login, name="login"),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/register/$', CustomRegistrationView.as_view()),
    url(r'^review/$', ApplicationReviewView().as_view()),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/resend_email', ResendEmail.as_view()),
    url(r'^accounts/is_active', is_active)
]
