from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView
from django.conf.urls import url
urlpatterns=[
    #path('user_login', views.user_login, {'register':False},name='user_login'),
    path('user_login', views.user_login,  name='user_login'),

    path('user_register',views.user_register,name='user_register'),
    path('logout',views.logout,name='logout'),
    path('del_user',views.del_user,name='del_user'),
    #path('admin_login', views.user_login, {'register':True},name='admin_login'),
    path('admin_register',views.admin_register,name='admin_register'),
    path('change_password', views.change_password, name='change_password'),

    path('reset-password',PasswordResetView.as_view(),name='password-reset'),
    path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]