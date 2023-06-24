import mimetypes
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from .models import Profile
from .models import Following
from blog.models import Post
from django.contrib.auth.models import User
from accounts.models import CustomUser
from django.contrib.auth.hashers import check_password

from django.core import validators
from django.core.exceptions import ValidationError
import re


def pic_upload(request):
    if request.method == "POST":
        file = request.FILES['profilePic']
        get_type = mimetypes.guess_type(str(file))
        img_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']

        if get_type[0] in img_types:
            user = CustomUser.objects.get(user=request.user)
            user.pic = file
            user.save()

            imgURL = 'https://img-static-s3.s3.amazonaws.com/media/profile/{image}'.format(image=file)
            return JsonResponse({'success': True, 'imgURL': imgURL })
        else:
            return JsonResponse({ 'success': False })
    return HttpResponse('Not valid response')


# under construction
def pic_delete(request):
    if request.method == "POST":
        file = request.POST.get('profilePic')
        getFile = request.POST.get('fileName')
        # print(file)
        # print(getFile)
        # s3 = boto3.resource("s3")
        # obj = s3.Object(file)

        # user = CustomUser.objects.get(user=request.user)
        # user.pic = file
        # user.save()
        return JsonResponse({'msg': 'success'})
    return HttpResponse('Working')


def follow(request, username):
    if request.user.is_authenticated and request.method == "POST":
        main_user = request.user
        to_follow = User.objects.get(username=username)
        following = Following.objects.filter(user=main_user, followed=to_follow)
        is_following = True if following else False 
        
        data = {}

        if is_following:
            Following.unfollow(main_user, to_follow)
            is_following = False
            data['following'] = False
            data['success'] = True
        else:
            Following.follow(main_user, to_follow)
            is_following = True
            data['following'] = True
            data['success'] = True
        return JsonResponse(data)
    else:
        data = {}
        data['success'] = False
        data['error'] = 'Please log in or create an account to follow'
        return JsonResponse(data)


def draft_post(request):
    if request.user.is_authenticated:
        get_user = User.objects.get(username=request.user).id

        posts = Post.objects.filter(user=get_user, published=False).order_by('-id')
        context = { 'posts': posts }
        return render(request, 'dashboard/draft-posts.html', context)
    else:
        return redirect('/login')


def published_post(request):
    if request.user.is_authenticated:
        get_user = User.objects.get(username=request.user).id

        posts = Post.objects.filter(user=get_user, published=True).order_by('-date')
        context = { 'posts': posts }
        return render(request, 'dashboard/published-posts.html', context)
    else:
        return redirect('/login')


def settings(request):
    if request.user.is_authenticated:
        get_user = request.user.id
        profile = Profile.objects.select_related(
            'user', 'user__customuser'
        ).get(user=get_user)

        context = { 'profile': profile }
        return render(request, 'dashboard/settings.html', context)
    else:
        return redirect('/login')


def profile_settings(request):
    if request.user.is_authenticated:
        get_user = request.user.id
        profile = Profile.objects.select_related(
            'user', 'user__customuser'
        ).get(user=get_user)

        context = { 'profile': profile }
        return render(request, 'components/profile-settings.html', context)
    else:
        return redirect("/login")


class EditProfile(View):
    def get(self, request):
        return HttpResponse('Not valid request')


    def validateName(self, name):
        if name == '' or name is None:
            self.data['name_error'] = 'Name cannot be blank'
            return False
        elif len(name) > 50:
            self.data['name_error'] = 'Name cannot greater then 50 characters'
            return False
        return True

    def validateUsername(self, username):
        if username is None or username == '':
            self.data['username_error'] = 'Username cannot be blank'
            return False

        username_regex = "^[a-zA-Z0-9_.-]+$"
        username_valid = re.match(username_regex, username)
        if username_valid is None:
            self.data['username_error'] = 'Username is not valid'
            return False
        return True


    def validateBio(self, bio):
        if bio == '' or bio is None:
            self.data['bio_error'] = 'Bio cannot be blank'
            return False
        elif len(bio) > 150:
            self.data['bio_error'] = 'Bio cannot be greater than 150 characters'
            return False
        return True


    def checkUsername(self, current_username, username):
        if current_username == username:
            return False
        elif current_username != username:
            username_taken = User.objects.filter(username=username
            ).exclude(username=current_username).exists()  
            
            if username_taken:
                self.data['username_error'] = 'Username already taken, try another'
                return False
            return True
        return False

    
    def checkName(self, current_name, name):
        if current_name == name:
            return False
        elif current_name != name:
            return True
        return False


    def checkURL(self, website):
        if website[:4] != 'http' and website != '':
            website_link = f'https://{website}'
            return website_link
        return website


    def post(self, request):
        if request.user.is_authenticated:
            name = request.POST.get('name', None)
            username = request.POST.get('username', None)
            bio = request.POST.get('bio', None)
            website = request.POST.get('website', None)

            self.data = {}

            self.validateName(name)
            self.validateUsername(username)
            self.validateBio(bio)

            if self.data == {}:
                current_user = request.user
                current_name = current_user.first_name

                Profile.objects.filter(user=current_user.id).update(
                    bio=bio, 
                    link=self.checkURL(website)
                )

                if self.checkName(current_name, name):
                    user = User.objects.get(first_name=request.user.first_name)
                    user.first_name = name
                    user.save()

                if self.checkUsername(current_user, username):
                    user = User.objects.get(username=request.user)
                    user.username = username
                    user.save()

                self.data['success'] = True
            else:
                self.data['success'] = False
            return JsonResponse(self.data)   


def account_settings(request):
    if request.user.is_authenticated:
        get_user = User.objects.get(username=request.user)
        context = { 'user': get_user }
        return render(request, 'components/account-settings.html', context)
    else:
        return redirect('/login')


class ChangeAccountSettings(View):
    def get(self, request):
        return HttpResponse('Not valid response')


    def validateEmail(self, emailID):
        try:
            validators.validate_email(emailID)
        except ValidationError:
            self.data['email_error'] = 'Not valid email'
            return False

        email_taken = User.objects.filter(email=emailID).exists()
        if email_taken:
            self.data['email_error'] = 'Email is already registered'
            return False
        return True

    
    def validatePassword(self, current_password, new_password):
        if len(current_password) < 8 or len(new_password) < 8:
            self.data['password_error'] = 'Password cannot be less then 8 characters'
            return False
        return True


    def post(self, request, param):
        if request.user.is_authenticated:
            self.data= {}

            if param == 'email':
                user_email = request.POST.get('email', None)
                if self.validateEmail(user_email):
                    current_email = User.objects.filter(email=user_email).exists()
                    
                    if not current_email:
                        user = User.objects.get(username=request.user)
                        user.email = user_email
                        user.save()

                        self.data['success'] = True
                else:
                    self.data['success'] = False
            elif param == 'password':
                current_pass = request.POST.get('current_pass', None)
                new_pass = request.POST.get('new_pass', None)

                if self.validatePassword(current_pass, new_pass):
                    if current_pass == new_pass:
                        self.data['success'] = True
                    elif current_pass != new_pass:
                        user = User.objects.get(username=request.user)
                        get_pass = check_password(current_pass, user.password)

                        if get_pass:
                            user.set_password(new_pass)
                            user.save()
                            self.data['success'] = True
                        else:
                            self.data['success'] = False
                            self.data['password_error'] = 'Current password is not correct'
            return JsonResponse(self.data)         
        return HttpResponse('Not valid request')
