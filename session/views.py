from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from session.forms import SignUpForm
from django.http import request


from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def loginuser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/tuition/home/')
            else:
                messages.error(request, 'Invalid Username or password')
        else:
            messages.error(request, 'Invalid Username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'session/login.html', {'form': form})


def logoutuser(request):
    logout(request)
    messages.error(request, 'Successfully logout')
    return redirect('/tuition/home/')


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            mail_subject = 'An account created'
            message = render_to_string('session/account.html', {
                'user': user,
                'domain': current_site.domain
            })
            text_contet=strip_tags(message)
            send_mail = form.cleaned_data.get('email')
            email = EmailMultiAlternatives(mail_subject, text_contet, to=[send_mail])
            email.attach_alternative(message,"text/html")
            email.send()
            return redirect('/session/login')
    else:
        form = SignUpForm()
    return render(request, 'session/signup.html', {'form': form})

def changepassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # update_session_auth_hash(request,form.user)
            messages.success(request,"Password successfully changed") 
            return redirect('/tuition/home/')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'session/change_pass.html',{'form':form})
