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
    url(r'^show_scholarship_template/(?P<x>[0-9]+)/(?P<y>[0-9]+)$', views.show_scholarship_template, name='show_template_sorted'),
    url(r'^change_status/(?P<x>[0-9]+)/(?P<y>[0-9]+)/(?P<z>[0-9]+)/$', views.change_status,name='change_status'),
    url(r'^show_scholarship_template/pdf/(?P<x>[0-9]+)/$', views.pdf_view, name='show-pdf'),
    url(r'^show_scholarship_template/scholarship_application_form/(?P<x>[0-9]+)/$', views.pdf_view2, name='show-scholarship-form'),
    url(r'^show_scholarship_template/applied_scholarship_application_form/(?P<x>[0-9]+)/$', views.pdf_view3,name='show-applied_scholarship-form'),
    url(r'^submit_application/(?P<x>[0-9]+)/(?P<y>[0-9]+)/$', views.submit_application, name='submit_application_form'),
    url(r'^applied_application/(?P<x>[0-9]+)/(?P<y>[0-9]+)/(?P<z>[0-9]+)/$', views.applied_application, name='applied_application'),
    path('simple_upload', views.simple_upload, name='simple_upload'),
    url(r'^simple_export/(?P<x>[0-9]+)/$',views.simple_export,name='simple_export'),
    url(r'^simple_export_admin_pannel/(?P<x>[0-9]+)/$', views.simple_export_admin_pannel, name='simple_export_admin_pannel'),

    url(r'^show_selected_applicants/(?P<x>[0-9]+)/$', views.show_selected_applicants, name='show_selected_applicants'),
    url(r'^confirm_selection/(?P<x>[0-9]+)/$', views.confirm_selection, name='confirm_selection'),
    url(r'^change_session/$', views.change_session, name='change_session'),
    url(r'^alter_session/(?P<flag>[0-9]+)/$', views.alter_session, name='alter_session'),
    url(r'^delete_previous_app/$', views.delete_previous_app, name='delete_previous_app'),
    url(r'^delete_all_students/$', views.delete_all_students, name='delete_all_students'),
    url(r'^delete_all_scholarships/$', views.delete_all_scholarships, name='delete_all_scholarships'),

    path('registered_students',views.registered_students,name = "registered_students"),
    url(r'^delete_student/(?P<x>[0-9]+)/$', views.delete_particular_student, name='delete_particular'),
    url(r'^delete_student_all/(?P<x>[0-9]+)/$', views.delete_all_student, name='delete_all_students'),
    path('our_team', views.our_team, name="our_team"),
    path('how_to_apply', views.how_to_apply, name="how_to_apply"),

]
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)