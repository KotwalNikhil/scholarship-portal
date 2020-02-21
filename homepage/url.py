from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url



urlpatterns = [
    path('', views.home, name="home"),
   # path('user_profile',views.user_profile,name='profile'),
    path('basic', views.basic, name='basichtml'),
    url(r'^application_form/(?P<x>[0-9]+)/$', views.show_application_form, name='application_form'),
    url(r'^show_scholarship_template/(?P<x>[0-9]+)/$',views.show_scholarship_template,name='show_template'),
    url(r'^show_scholarship_template/pdf/(?P<x>[0-9]+)/$', views.pdf_view, name='show-pdf'),

]
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)