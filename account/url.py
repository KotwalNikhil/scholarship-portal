from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
    #path('user_login', views.user_login, {'register':False},name='user_login'),
    path('user_login', views.user_login,  name='user_login'),

    path('user_register',views.user_register,name='user_register'),
    path('logout',views.logout,name='logout'),
    path('del_user',views.del_user,name='del_user'),
    path('user_profile',views.user_profile,name='profile'),
    path('show_user_profile_for_admin_work/',views.show_user_profile_for_admin_work,name='show_user_profile_for_admin_work'),
    path('edit_user_profile_form/', views.edit_user_profile_form, name='edit_user_profile_form'),
    url(r'^edit_user_profile_for_admin_work/(?P<x>[0-9]+)/$', views.edit_user_profile_for_admin_work,name='edit_user_profile_for_admin_work'),
    path('admin_register',views.admin_register,name='admin_register'),
    url(r'^admin_delete/(?P<x>[0-9]+)/$', views.admin_delete, name='admin_delete'),

    path('change_password', views.change_password, name='change_password'),

    path('reset-password',PasswordResetView.as_view(),name='password-reset'),
    path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)