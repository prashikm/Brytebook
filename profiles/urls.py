from django.urls import path
from . import views
from profiles.views import EditProfile, ChangeAccountSettings


urlpatterns = [
    # account user's profile & profile settings
    path('profile/edit', views.profile_settings, name='profile_edit'),
    path('profile/edit_profile', EditProfile.as_view(), name='edit_profile'),
    path('profile/pic/upload', views.pic_upload, name='pic_upload'),
    path('profile/pic/delete', views.pic_delete, name='pic_delete'),

    # account user's posts
    path('i/post/draft', views.draft_post, name="draft_post"),
    path('i/post/published', views.published_post, name="published_post"),

    # account user's settings
    path('i/settings', views.settings, name="settings"),
    path('i/account-settings', views.account_settings, name="account_settings"),
    path('i/settings/<str:param>/', ChangeAccountSettings.as_view(), name='change_account_settings'),

    # follow url
    path('follow/<str:username>', views.follow, name='follow'),
]
