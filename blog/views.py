import datetime
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from profiles.models import Following
from django.contrib.auth.models import User
from profiles.models import Profile
from django.http import HttpResponse
from datetime import datetime
from django.template.defaultfilters import default, slugify
import urllib
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
import boto3
import os
import mimetypes
from django.db.models import Q
from django.views import View


def home_feed(request):
    if request.user.is_authenticated:
        posts_list = Post.objects.filter(published=True).select_related(
            'user', 'user__customuser'
        ).order_by('-date')

        page = request.GET.get('page', 1)
        paginator = Paginator(posts_list, 6)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = { 'posts': posts }
        return render(request, 'profile/homefeed.html', context)
    else:
        return redirect('/login')


def search_result(request):
    if request.user.is_authenticated:
        query = request.GET.get('q', default='')

        if len(query) > 78:
            posts = []
            context = { 'query': query }
        else:
            posts_list = Post.objects.filter(Q(title__icontains=query, 
                published=True) | Q(desc__icontains=query, 
            published=True)).select_related(
                'user', 'user__customuser'
            ).order_by('-date')

            page = request.GET.get('q', 1)
            paginator = Paginator(posts_list, 6)

            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            context = { 'posts': posts, 'query': query }
        return render(request, 'profile/search.html', context)
    else:
        return redirect('/login')


def search_page(request):
    if request.user.is_authenticated:
        return render(request, 'profile/search-posts.html')
    else:
        return redirect('/login')


def article(request, username, id, slug):
    try:
        post = Post.objects.filter(id=id, slug=slug).select_related(
            'user', 'user__customuser'
        ).first()
        profile = Profile.objects.get(user=post.user)

        user_posts = Post.objects.filter(user=post.user, 
            published=True).select_related(
                'user'
            ).exclude(slug=slug).order_by('-date')
        
        share_string = urllib.parse.quote_plus(post.title)

        if request.user.is_authenticated:
            the_following = Following.objects.filter(user=request.user, 
                followed=post.user)
            is_following = True if the_following else False

            the_curated = post.curate.filter(username=request.user)
            is_curated = True if the_curated else False
        else:
            is_curated = False
            is_following = False

        context = {
            'post': post, 
            'user_posts': user_posts, 
            'share_string': share_string, 
            'profile': profile, 
            'is_following': is_following,
            'is_curated': is_curated
        }
        return render(request, 'posts/post-structure.html', context)
    except AttributeError:
        return redirect('/home')


def curate_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            get_user = request.user
            user_id = request.user.id

            data = {}

            post = get_object_or_404(Post, id=post_id)
            post_exists = post.curate.filter(id=user_id).exists()
            if post_exists:
                post.curate.remove(get_user)
                data['removed'] = 'Removed'
            else:
                post.curate.add(get_user)
                data['added'] = 'Added'
            return JsonResponse(data)
        return JsonResponse({ "error": "Not valid request!" })
    else:
        data = {}
        data['error'] = 'Please log in or create an account to curate'
        return JsonResponse(data)


def profile(request, user):
    try:
        get_user = User.objects.get(username=user).id
        profile = Profile.objects.select_related(
            'user', 'user__customuser'
        ).get(user=get_user)
        posts = Post.objects.filter(user=get_user, published=True).select_related(
            'user', 'user__customuser'
        ).order_by('-date')

        if request.user.is_authenticated:
            the_following = Following.objects.filter(
                user=request.user, followed=get_user
            )
            is_following = True if the_following else False
        else:
            is_following = False
            
        follower = Following.objects.filter(followed__username=user).count()
        following = User.objects.filter(follow__user=get_user).count()

        context = {
            'profile': profile, 
            'posts': posts, 
            'follower': follower, 
            'following': following, 
            'is_following': is_following
        }
        return render(request, 'profile/profile.html', context)
    except ObjectDoesNotExist:
        return redirect('/home')


def curated_posts(request, username):
    if request.user.is_authenticated:
        try:
            get_user = User.objects.get(username=username)
            user_id = get_user.id

            profile = Profile.objects.select_related(
                'user', 'user__customuser'
            ).get(user=user_id)

            posts  = get_user.curate.all().select_related(
                'user', 'user__customuser'
            ).order_by('-date')
            follower = Following.objects.filter(followed__username=request.user).count()
            following = User.objects.filter(follow__user=user_id).count()

            try:
                the_following = Following.objects.filter(
                    user=request.user, followed=get_user
                )
                is_following = True if the_following else False
            except TypeError:
                is_following = False

            context = {
                'profile': profile, 
                'posts': posts, 
                'follower': follower, 
                'following': following,
                'is_following': is_following,
            }
            return render(request, 'profile/curated.html', context)
        except ObjectDoesNotExist:
            return redirect('/home')
    else:
        return redirect('/login')


def get_user_post(request, user, type_of):
    if request.method == "POST":
        if type_of == 'posts':
            get_user = User.objects.get(username=user).id
            posts = Post.objects.filter(user=get_user, 
                published=True).select_related(
                    'user', 'user__customuser'
                ).order_by('-date')
            context = { 'posts': posts }
            return render(request, 'components/blog-posts.html', context)
        else:
            get_user = User.objects.get(username=user)
            posts = posts = get_user.curate.all().select_related(
                'user', 'user__customuser'
            ).order_by('-date')
            context = { 'posts': posts }
            return render(request, 'components/blog-posts.html', context)
    return HttpResponse('Not valid request')


def followers_list(request, username):
    user_pic = User.objects.select_related(
        'customuser'
    ).get(username=username)
    follower_list = Following.objects.filter(followed__username=username
    ).select_related('user', 'user__customuser')
    context = { 'follower': follower_list, 'list_user': user_pic }
    return render(request, 'profile/followers_list.html', context)


def following_list(request, username):
    the_user = User.objects.select_related(
        'customuser'
    ).get(username=username)

    following_list = User.objects.filter(follow__user=the_user.id
    ).select_related('customuser', 'following')
    context = { 'follower': following_list, 'list_user': the_user }
    return render(request, 'profile/following_list.html', context)


def bookmarks(request):
    if request.user.is_authenticated:
        get_user = User.objects.get(username=request.user)

        posts = get_user.bookmark.all().order_by('-date')
        context = {'posts': posts}
        return render(request, 'profile/bookmarks.html', context)
    else:
        return redirect('/login')


def bookmark_this(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            get_user = request.user
            user_id = get_user.id

            data = {}

            post = get_object_or_404(Post, id=post_id)
            if post.bookmark.filter(id=user_id).exists():
                post.bookmark.remove(get_user)
                data['removed'] = 'Removed'
            else:
                post.bookmark.add(get_user)
                data['added'] = 'Added'
            return JsonResponse(data)
        return JsonResponse({ 'error': 'Not valid request' })
    else:
        data = {}
        data['error'] = 'Please log in or create an account to bookmark'
        return JsonResponse(data)


def new_post(request):
    if request.user.is_authenticated:
        return render(request, 'posts/new-post.html')
    else:
        return redirect('/login')


# add image type validations, take inspiration from profile image upload view
def upload_cover(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            get_user = request.user.id
            file = request.FILES['coverImg']
            get_type = mimetypes.guess_type(str(file))

            s3 = boto3.client('s3',
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
            )

            s3.upload_fileobj(file,
                os.environ['AWS_STORAGE_BUCKET_NAME'],
                'cover/{user_id}/{file}'.format(user_id=get_user, file=file),
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': get_type[0]
                }
            )
            get_url = 'https://img-static-s3.s3.us-west-2.amazonaws.com/cover/{user_id}/{file}'.format(user_id=get_user, file=file)
            data = {}
            data['success'] = True
            data['url'] = get_url
            return JsonResponse(data)
        return JsonResponse({ 'Not valid response' })
    else:
        return redirect('/login')


def img_upload(request):
    '''
    This function upload any incoming file upload request from post content to it's file location.
    The upload location is aws.bucket.name/post/user_id/filename.
    '''
    if request.user.is_authenticated:
        if request.method == "POST":
            get_user = request.user.id
            file = request.FILES['upload']

            get_type = mimetypes.guess_type(str(file))
            s3 = boto3.client('s3',
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
            )

            s3.upload_fileobj(file,
                os.environ['AWS_STORAGE_BUCKET_NAME'],
                'post/{user_id}/{file}'.format(user_id=get_user, file=file),
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': get_type[0]
                }
            )

            return JsonResponse({
                'url': 'https://img-static-s3.s3.us-west-2.amazonaws.com/post/{user_id}/{file}'.format(user_id=get_user, file=file)
            })
        return JsonResponse({'error': 'Invalid response'})
    else:
        return redirect('/login')


class CheckContent:
    def checkTitle(self, title):
        get_title_len = len(title)
        if get_title_len < 12:
            self.data['title_error'] = 'Title is too short'
            return False
        elif get_title_len > 120:
            self.data['title_error'] = 'Title is too long'
            return False
        return True


    def checkContent(self, content):
        if content == '':
            self.data['content_error'] = 'Content is too short'
            return False
        return True


class PublishContent(View, CheckContent):
    def get(self, request):
        return redirect('/login')


    def post(self, request):
        if request.user.is_authenticated:
            post_id = request.POST.get('id', None)
            title = request.POST.get('title', None)
            content = request.POST.get('content', None)
            cover_image = request.POST.get('coverImg', default='NotChanged')
            img_changed = request.POST.get('img', default='false')

            self.data = {}

            self.checkTitle(title)
            self.checkContent(content)

            if self.data == {}:
                self.data['success'] = True
                if post_id == 'undefined':
                    posts = Post(user=request.user,
                        title=title,
                        slug=slugify(title),
                        cover=cover_image,
                        desc=content,
                        date=datetime.today(),
                        published=True
                    )
                    posts.save()
                    self.data['redirect'] = True
                else:
                    post = Post.objects.get(id=post_id)
                    if str(post.date) == '2021-05-08':
                        post.date = datetime.today()
                        post.save()

                    if img_changed =='true' and str(cover_image) != '':
                        post.title = title
                        post.desc = content
                        post.cover = cover_image
                        post.published = True
                        post.save()
                    elif img_changed == 'false' and cover_image == 'NotChanged':
                        post = Post.objects.filter(id=post_id).update(
                            title=title, 
                            slug=slugify(title), 
                            desc=content, 
                            published=True
                        )
            else:
                self.data['success'] = False
            return JsonResponse(self.data)
        return redirect('/login')


class DraftContent(View, CheckContent):
    def get(self, request):
        return redirect('/login')


    def post(self, request):
        if request.user.is_authenticated:
            post_id = request.POST.get('id', None)
            title = request.POST.get('title', None)
            content = request.POST.get('content', None)
            cover_img = request.POST.get('coverImg', default='NotChanged')
            img_changed = request.POST.get('img', default='false')

            self.data = {}

            self.checkTitle(title)
            self.checkContent(content)

            if self.data == {}:
                self.data['success'] = True
                if post_id == 'undefined':
                    posts = Post(user=request.user,
                        title=title,
                        slug=slugify(title),
                        cover=cover_img,
                        desc=content,
                        published=False
                    )
                    posts.save()
                    self.data['redirect'] = True
                elif img_changed == 'true' and str(cover_img) != '':
                    post = Post.objects.get(id=post_id)
                    post.title = title
                    post.desc = content
                    post.cover = cover_img
                    post.published = False
                    post.save()
                elif img_changed == 'false' and cover_img == 'NotChanged':
                    post = Post.objects.filter(id=post_id).update(
                        title=title, 
                        slug=slugify(title), 
                        desc=content, 
                        published=False
                    )
            else:
                self.data['success'] = False  
            return JsonResponse(self.data)
        return redirect('/login')


def get_edit_post(request, the_id, the_slug):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(id=the_id, slug=the_slug)
            context = { 'post': post }
            return render(request, 'posts/editing_post.html', context)
        except Post.DoesNotExist:
            return redirect('/account/i/post/draft')
    else:
        return redirect('/login')


def delete_post(request, post_id, post_slug):
    if request.user.is_authenticated:
        if request.method == 'DELETE':
            Post.objects.filter(user=request.user, id=post_id, 
                slug=post_slug).delete()
            return HttpResponse('')
    return HttpResponse('Not valid response')
