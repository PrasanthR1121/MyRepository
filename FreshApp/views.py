from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required
def home(request):
    return HttpResponse("HOME PAGE")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))

def index(request):
    return HttpResponse("INDEX PAGE")

def register(request):
    if request.method == "POST":
        userprofileform = UserProfileForm(request.POST)
        userportfolioform = PortfolioForm(request.POST)
        if userprofileform.is_valid() and userportfolioform.is_valid():
            user = userprofileform.save(commit=False)
            user.set_password(userprofileform.cleaned_data['password'])
            user.save()
            portfolio = userportfolioform.save(commit=False)
            portfolio.user = user
            if 'profile_pic' in request.FILES:
                portfolio.profile_pic = request.FILES['profile_pic']
            else:
                print("NO FILES")
            portfolio.save()
        else:
            print("FORM IS INVALID")
    else:
        userprofileform = UserProfileForm()
        userportfolioform = PortfolioForm()
    con = {'user_form': userprofileform, 'user_portfolio': userportfolioform}
    return render(request, "registration.html", con)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('register'))
            else:
                return HttpResponse("ACCOUNT IS INACTIVE")
        else:
            print(f"SOMEONE IS TRIED TO LOGIN BUT FAILED , USERNAME = {username} and PASSWORD = {password}")
            return HttpResponse("INVALID CREDENTIALS")
    else:
        return render(request, "login.html")

@login_required
def reg(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password_1 = request.POST.get("password")
        password_2 = request.POST.get("confirm_password")
        gender = request.POST.get("gender")

        if password_1 == password_2:
            obj = register_model.objects.create(name=name, username=username, email=email, phone=phone, password=password_1, gender=gender)
            if obj:
                obj.save()
                HtmlMessage = render_to_string('Email_Template.html', {"variable": 'value'})
                PlainText = strip_tags(HtmlMessage)
                Email = EmailMultiAlternatives(
                    subject="Sample Email",
                    body=PlainText,
                    from_email="prasanthrajan1121@gmail.com",
                    to=[email, "vinsshaji2@gmail.com", "praveenpopz82@gmail.com"]
                )
                Email.attach_alternative(HtmlMessage, "text/html")
                Email.send()
                return HttpResponse("Data saved to db successfully!!!")
            else:
                return HttpResponse("Something happened while we are creating object for the model")
        else:
            pss = True
            return render(request, "Reg.html", {"pass": pss})

    else:
        return render(request, "Reg.html")

@login_required
def update(request):
    if request.method == 'POST':
        user_email = request.user.email
        details = get_object_or_404(register_model, email=user_email)
        details.name = request.POST.get("name")
        details.username = request.POST.get("username")
        details.email = request.POST.get("email")
        details.phone = request.POST.get("phone")
        p1 = request.POST.get("password")
        p2 = request.POST.get("confirm_password")
        if p1 == p2:
            details.password = p1
        details.gender = request.POST.get("gender")
        details.save()
        return HttpResponse("Data updated to DB successfully !!!")
    else:
        user_email = request.user.email
        print(user_email)
        details = get_object_or_404(register_model, email=user_email)
        con = {"det": details}
        return render(request, "update.html", con)

def Sample(request):
    return render(request, "Sample.html")

@login_required
@require_POST
def delete(request, email):
    try:
        details = get_object_or_404(register_model, email=email)
        details.delete()
        return HttpResponse("Deleted Successfully")
    except Http404:
        return HttpResponse("User not found ", status=404)

@login_required
def data_visual(request):
    email = request.user.email
    details = get_object_or_404(register_model, email=email)
    return render(request, "user_details.html", {"det": details,"email":email})


