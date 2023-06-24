import os
import re
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.db import IntegrityError
from profiles.models import Profile
from .models import Invitation
from django.views import View

import requests
from django.core import validators
from django.core.exceptions import ValidationError

from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from blog.models import Post


def landing(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        posts = Post.objects.filter(published=True).select_related(
            'user', 'user__customuser'
        ).order_by('-date')[:4]
        context = { 'posts': posts}
        return render(request, 'landing.html', context)


def explore(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        posts = Post.objects.filter(published=True).select_related(
            'user', 'user__customuser'
        ).order_by('-date')[:8]

        context = { 'posts': posts }
        return render(request, 'home.html', context)


def announcement(request):
    return render(request, 'brytebook-announcement.html')


def privacy_policy(request):
    return render(request, 'policies/privacy-policy.html')


def terms(request):
    return render(request, 'policies/terms.html')


def donate(request):
    return render(request, 'donate.html')


def invite_user(request):
    if request.user.is_authenticated and (request.user.username == 'prashik') or (request.user.username == 'samyak'):
        if request.method == "POST":
            email = request.POST.get('email')
            invite = Invitation(email=email)
            invite.save()
            return redirect('/get/invite/user')
        getInvite = Invitation.objects.all().reverse()
        context = { 'invites': getInvite }
        return render(request, 'invite-user.html', context)
    else:
        return HttpResponse('You do not have access!')


# Work Under Progress 
def send_to_user(request):
    if request.user.is_authenticated and request.user.username == 'prashik':
        if request.method == "POST":
            get_email = 'prashikm861@gmail.com'
            name = request.POST.get('name')
            message = request.POST.get('message')

            context = {
                'name': name,
                'message': message
            }
            html_content = render_to_string('email_template.html', context)
            text_content = strip_tags(html_content)

            # email= EmailMultiAlternatives(
            #     # subject
            #     'This is the hello subject',

            #     # content
            #     text_content,

            #     # from
            #     'prashikcodes@gmail.com',

            #     # to
            #     [get_email]
            # )

            # email.attach_alternative(html_content, 'text/html')
            # email.send()

            return redirect('/send/mail/user')
        return render(request, 'send-to-mail.html')
    else:
        return HttpResponse('You have not access')


def get_early_access(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            validate_email = validators.validate_email(email)

            if validate_email is None:
                url = 'https://getwaitlist.com/api/v1/waitlists/submit'
                the_data = {
                    "email": email,
                    "api_key": os.environ['GETWAITLIST_API_KEY'],
                    "referral_link": "https://brytebook.com"
                }
                make_request = requests.post(url, json=the_data)
                success = True
                make_request = make_request.json()
        except ValidationError:
            success = False

        if success:
            context = {
                'current_priority': make_request.get('current_priority'),
                'referral_link': make_request.get('referral_link'),
            }
            return render(request, 'early-access.html', context=context)
        else:
            return render(request, 'error-early-access.html', context={ 'error': 'Not valid email' })
    return render(request, '/get-early-access')


class LoginValidation:
    def validateEmail(self, emailID):
        try:
            validators.validate_email(emailID)
        except ValidationError:
            self.data['email_error'] = 'Not valid email'
            return False

        self.email_taken = User.objects.filter(email=emailID)
        if not self.email_taken.exists():
            self.data['email_error'] = 'Email is not registered'
            return False
        return True


    def validatePassword(self, password):
        if len(password) < 8:
            self.data['password_error'] = 'Password cannot be less than 8 characters'


    def checkEmailPass(self, password):
        if self.email_taken.exists():
            isUser = self.email_taken.first().check_password(password)

            if not isUser:
                self.data['some_error'] = 'Your email or password is not valid, check again!'
                return False
        return True
    

class LoginUser(View, LoginValidation):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/home')
        else:
            return render(request, 'auth/login.html')

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        self.data = {}

        self.validateEmail(email)
        self.validatePassword(password)
        self.checkEmailPass(password)

        if self.data == {}:
            self.data['success'] = True
            user = authenticate(username=email, password=password)

            if user is not None:
                auth_login(request, user)
            else:
                self.data['success'] = False
        else:
            self.data['success'] = False
        return JsonResponse(self.data)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data)|Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset/password_reset_email.html"
                    c = {
                        "email": user.email,
                        "domain": 'brytebook.com',
                        "site_name": 'Brytebook',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    text_content = strip_tags(email)
                    try:
                        msg = EmailMultiAlternatives(
                            subject,
                            text_content,
                            'brytebookhq@gmail.com',
                            [user.email],
                            headers={ 'Reply-To': 'brytebookhq@gmail.com' }
                        )
                        msg.attach_alternative(email, 'text/html')
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found')
                    return redirect('/password_reset/done/')
    password_reset_form = PasswordResetForm()
    return render(request, 'password_reset/password_reset.html', context={ 'form': password_reset_form })


def logout_user(request):
    logout(request)
    messages.success(request, 'You are successfully logged out')
    return redirect('/login')


def signup(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        invite_code = request.GET.get('invite', None)
        return render(request, 'auth/signup.html', context={ 'invite_code': invite_code })


class SignUpValidations:
    def validateInvite(self, invite_code):
        invite_re = '^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z'
        invite_valid = re.match(invite_re, invite_code)

        if invite_valid is None:
            return False
        return True


    def validateCodeUsed(self, code):
        try:
            print('Working', code)
            self.getCode = Invitation.objects.get(invitation_code=code)
            if self.getCode.code_applied:
                return False
        except Invitation.DoesNotExist:
            return False
        return True

    
    def validateUsername(self, username):
        username_regex = "^[a-zA-Z0-9_.-]+$"
        username_valid = re.match(username_regex, username)
        if username_valid is None:
            self.data['username_error'] = 'Username is not valid'
            return False

        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            self.data['username_error'] = 'Username is already taken, try another'
            return False
        return True 


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


class ValidateSignup(View, SignUpValidations):
    def get(self, request):
        return HttpResponse('Not at valid response')

    def post(self, request):
        self.invite = request.POST.get('invite')
        self.username = request.POST.get('username', None)
        self.email = request.POST.get('email', None)
        self.password = request.POST.get('password', None)

        self.data = {}

        if not self.validateInvite(self.invite):
            self.data['invite_error'] = 'Not valid code'
        elif not self.validateCodeUsed(self.invite):
            self.data['invite_error'] = 'Code already used or not valid'

        self.validateUsername(self.username)
        self.validateEmail(self.email)
        self.validateEmail(self.email)


        if len(self.password) < 8:
            self.data['password_error'] = "Password cannot be less than  8 characters"

        if self.data == {}:
            self.data['success'] = True

            self.getCode.code_applied=True
            self.getCode.save()

            try:
                user = User.objects.create_user(self.username, 
                    self.email, self.password
                )
                user.save()

                # send mail here...

                auth_user = authenticate(username=self.email, 
                    password=self.password
                )

                if auth_user is not None:
                    auth_login(request, user)
                else:
                    return HttpResponse('Not valid user')
            except IntegrityError:
                return HttpResponse('Not valid response')
        else:
            self.data['success'] = False
        
        self.data['message'] = 'Doing some request'
        return JsonResponse(self.data)


class SetupProfile(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'auth/setup-profile.html')
        else:
            return redirect('/signup')
    

    def validateName(self, name):
        if len(name) < 1:
            self.data['name_error'] = 'Name cannot be empty'
            return False
        elif len(name) > 50:
            self.data['name_error'] = 'Name cannot greater then 50 characters'
            return False
        return True


    def validateBio(self, bio):
        if len(bio) < 1:
            self.data['bio_error'] = 'Bio cannot be empty'
            return False
        elif len(bio) > 150:
            self.data['bio_error'] = 'Bio cannot greater then 150 characters'
            return False
        return True


    def post(self, request):
        name = request.POST.get('name', None)
        bio = request.POST.get('bio', None)

        self.data = {}

        self.validateName(name)
        self.validateBio(bio)

        if self.data == {}:
            self.data['success'] = True

            get_user = User.objects.get(username=request.user)
            get_user.first_name = name
            get_user.save()

            user_id = get_user.id
            Profile.objects.filter(user=user_id).update(bio=bio)
        else:
            self.data['success'] = False
        
        return JsonResponse(self.data)


def finished(request):
    if request.user.is_authenticated:
        return render(request, 'auth/finished.html')
    else:
        return redirect('/signup')


def delete_account(request, username):
    if request.user.is_authenticated and request.method == "POST":
        if request.user == username:
            password = request.POST.get('password', None)

            user_exists = User.objects.get(username=username)
            if user_exists:
                correct_user = user_exists.check_password(password)
                if correct_user:
                    logout(request)

                    u = User.objects.get(id=user_exists.id)
                    u.delete()

                    messages.success(request, 'Successfully deleted your account')
                    return redirect('/signup')
                return redirect('/account/i/settings')
        return redirect('/account/i/settings')
    return redirect('/account/i/settings')
