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
    url(r'^$',views.Login),
    url(r'^signup/$',views.signup),
    url(r'^login/$',views.Login),
    url(r'^logout/$',views.Logout),
    url(r'^myProfile/$',views.my_profile),
    url(r'^friendProfile/$',views.friend_profile),
    url(r'^newsfeed/$',views.view_newsfeed),
    url(r'^connections/$',views.view_connections),
    url(r'^matchRequest/$',views.send_match_request),
    url(r'^accept/$',views.accept,name='accept'),
    url(r'^reject/$',views.reject,name='reject'),
    url(r'^search/$',views.search,name='search'),
    url(r'^create/$',views.createUser,name='create'),
    url(r'^deleteRequest/$',views.deleteRequest),
    url(r'^settings/$',views.settings),
    url(r'^editRequest/(?P<scheduleID>[0-9]+)/$',views.editRequest,name='editRequest'),
    url(r'^makeConnections/$',views.create_connection,name='makeConnection'),
    url(r'^admin/',include(admin.site.urls)),
    url('',include('social_django.urls',namespace='social')),
    url('',include('django.contrib.auth.urls',namespace='auth')),
    url('^gc/$',views.listCalendar,name='listCalendar'),

]
#commit