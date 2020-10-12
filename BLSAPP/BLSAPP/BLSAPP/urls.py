"""BLSAPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import django
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from graphene_django.views import GraphQLView
from BLSAPP.schema import schema
from api.errors import CustomGraphQLView
import api.views
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

from api.restViews import rest_get_blsEvents , rest_del_blsEvents , rest_set_blsEvents , rest_get_blsAlarms , rest_del_blsAlarms , rest_set_blsAlarms
from api.restViews import availableMethods
from api.admin import getAdmin , getEmpty


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', getEmpty),
    path('admin', getAdmin),
    path('admin/', getAdmin),
    path('graphql/', CustomGraphQLView.as_view(graphiql=True)) ,
    path('rest' , availableMethods) , 
    path('rest/' , availableMethods) , 
    path('rest/get_blsEvents', rest_get_blsEvents),
	path('rest/del_blsEvents', rest_del_blsEvents),
	path('rest/set_blsEvents', rest_set_blsEvents),
	path('rest/get_blsAlarms', rest_get_blsAlarms),
	path('rest/del_blsAlarms', rest_del_blsAlarms),
	path('rest/set_blsAlarms', rest_set_blsAlarms)
]

handler400 = 'api.views.bad_request'
handler403 = 'api.views.permission_denied'
handler404 = 'api.views.page_not_found'
handler500 = 'api.views.server_error'
