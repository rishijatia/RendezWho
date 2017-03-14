"""RendezWho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.login),
    url(r'^signup/$',views.signup),
    url("^soc/", include("social_django.urls", namespace="social")),
    url(r'^login/$',views.login),
    url(r'^myProfile/$',views.my_profile),
    url(r'^friendProfile/$',views.friend_profile),
    url(r'^newsfeed/$',views.view_newsfeed),
    url(r'^connections/$',views.view_connections),
    url(r'^matchRequest/$',views.send_match_request),
    url(r'^search/$',views.search),
    url(r'^settings/$',views.settings),
]
#commit