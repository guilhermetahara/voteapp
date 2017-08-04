"""voteapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from voto import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #localhost:8000/
    url(r'^$', views.home, name='home'),

    #localhost:8000/usuario/cad
    url(r'^usuario/cad$', views.createuser, name='createuser'),

    #localhost:8000/login
    url(r'^login/$', views.userlogin, name='login'),

    ##localhost:8000/logout
    url(r'^logout/$', views.userlogout, name='logout'),

    #localhost:8000/usuario/<username>/
    url(r'^usuario/(?P<username>[\w.@+-]+)/$', views.Userindex.as_view(), name='userindex'),

    #localhost:8000/usuario/<username>/votacao/<pergunta>
    url(r'^usuario/(?P<username>[\w.@+-]+)/votacao/.*$', views.Votacao.as_view(), name='votacao'),

]