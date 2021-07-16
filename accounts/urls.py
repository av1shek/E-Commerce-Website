from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views

app_name='accounts'

urlpatterns = [
    url(r'home/', views.home, name='home'),
    # url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    # url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),


    url(r'^signup/$', views.signup, name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             success_url=reverse_lazy('accounts:password_reset_done'),
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('accounts:password_reset_complete'),
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    
]
