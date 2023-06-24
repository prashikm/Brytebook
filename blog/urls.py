from django.urls import path
from django.conf.urls import url
from . import views
from blog.views import DraftContent, PublishContent

urlpatterns = [
    # user's home page
    path('home', views.home_feed, name='home-feed'),

    # search
    path('search-posts', views.search_page, name='search_page'),
    path('search', views.search_result, name='search_result'),

    # user's all bookmarks
    path('bookmarks', views.bookmarks, name='bookmark'),

    # edit post
    path('edit/post/<int:the_id>-<str:the_slug>/', views.get_edit_post, name='get_edit_post'),

    # delete this post
    path('delete/<int:post_id>-<str:post_slug>', views.delete_post, name='delete_post'),

    # bookmark the article
    path('bookmark/post/<int:post_id>', views.bookmark_this, name='bookmark_this'),

    # follow/username -> follow a specific user
    # path('follow/<str:username>', views.follow, name='follow'),

    # create new post
    path('new-post', views.new_post, name='new_post'),
    path('upload-cover', views.upload_cover, name='upload_cover'),
    path('post/image/upload', views.img_upload, name='img_upload'),

    # publish the editior content
    url('publish_content', PublishContent.as_view(), name='publish_content'),
    url('draft_content', DraftContent.as_view(), name='draft_content'),

    # username/article -> article url
    path('<str:username>/<int:id>-<str:slug>', views.article, name='article'),

    # Curation
    path('curate/<int:post_id>', views.curate_post, name='curate_post'),
    path('<str:username>/curated', views.curated_posts, name='curated_posts'),

    # username -> user profile
    path('<str:username>/followers', views.followers_list, name='followers_list'),
    path('<str:username>/following', views.following_list, name='following_list'),
    path('<str:user>', views.profile, name='profile'),
    path('get-user-posts/<str:user>/<str:type_of>', views.get_user_post, name='get_user_post'),

]
