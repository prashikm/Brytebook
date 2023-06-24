from django.urls import path
from django.conf.urls import url
from . import views
from accounts.views import ValidateSignup, LoginUser, SetupProfile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing, name='landing_page'),
    path('announcement', views.announcement, name='announcement'),
    path('explore', views.explore, name='explore'),
    path('get-early-access', views.get_early_access, name='get_early_access'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('terms', views.terms, name='terms'),
    path('donate', views.donate, name='donate'),
    path('get/invite/user', views.invite_user, name='invite_user'),
    path('send/mail/user', views.send_to_user, name='send_to_user'),

    url(r'^login$', LoginUser.as_view(), name='login'),
    url(r'^logout$', views.logout_user, name='logout'),

    path('signup', views.signup, name='signup'),
    url(r'^signup/validate_signup/$', ValidateSignup.as_view(), name='validate_signup'),
    path('signup/setup-profile', SetupProfile.as_view(), name='setup-profile'),
    path('signup/finished', views.finished, name='finished'),

    url(r'^password_reset/$', views.password_reset_request, name='password_reset'),
    url(r'^password_reset/done/$',   
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), 
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), 
        name='password_reset_complete'
    ),

    path('account/delete/<str:username>', views.delete_account, name='delete_account'),
]
