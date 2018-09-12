"""warsztat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from mail_box.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('new', NewContact.as_view()),
    re_path(r'^modify/(?P<id>(\d)+)$', ModifyContact.as_view()),
    re_path(r'^delete/(?P<id>(\d)+)$', DeleteContact.as_view()),
    re_path(r'^show/(?P<id>(\d)+)$', ShowContact.as_view()),
    re_path(r'^(?P<id>(\d)+)/addAddress$', AddAddress.as_view()),
    re_path(r'^(?P<id>(\d)+)/addPhone$', AddPhone.as_view()),
    re_path(r'^(?P<id>(\d)+)/addEmail$', AddEmail.as_view()),
    path('addGroup', AddGroup.as_view()),
    path('groups', GroupList.as_view()),
    re_path(r'^group/(?P<id>(\d)+)$', ShowGroup.as_view()),
    path('', ShowAll.as_view()),
    re_path(r'^addParticipants/(?P<id>(\d)+)$', AddParticipant.as_view()),
    re_path(r'^deletePhone/(?P<id>(\d)+)$', DeletePhone.as_view()),
    re_path(r'^deleteEmail/(?P<id>(\d)+)$', DeleteEmail.as_view()),
    re_path(r'^deleteAddress/(?P<id>(\d)+)$', DeleteAddress.as_view()),
    # path('addPhoto', simple_upload.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)