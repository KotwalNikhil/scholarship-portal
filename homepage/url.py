from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url



urlpatterns = [
    path('', views.home, name="home"),
    path('add_scholarship',views.add_scholarship_function,name='add_scholarship'),
    path('basic', views.basic, name='basichtml'),
    url(r'^delete_scholarship/(?P<x>[0-9]+)/$', views.delete_scholarship, name='delete_scholarship'),
    url(r'^application_form/(?P<x>[0-9]+)/$', views.show_application_form, name='application_form'),
    url(r'^show_scholarship_template/(?P<x>[0-9]+)/$',views.show_scholarship_template,name='show_template'),
    url(r'^show_scholarship_template/pdf/(?P<x>[0-9]+)/$', views.pdf_view, name='show-pdf'),
    url(r'^submit_application/(?P<x>[0-9]+)/(?P<y>[0-9]+)/$', views.submit_application, name='submit_application_form'),

]
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)