from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models import Q

from .models import CustomUser


class SignupView(TemplateView):
    template_name = 'auth_app/signup.html'

    def validations(self, data):
        email = data.get('email')
        mobile = data.get('mobile')

        if CustomUser.objects.filter(email=email).exists():
            return False, "Duplicate Email Id"
        
        if CustomUser.objects.filter(mobile=mobile).exists():
            return False, "Duplicate Mobile Number"
        
        return True, "Valid Data"


    def post(self, request, *args, **kwargs):
        print(request.POST)
        is_valid, msg = self.validations(request.POST)

        if is_valid:
            user = CustomUser()
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.mobile = request.POST.get("mobile")
            user.address = request.POST.get("address")
            user.city = request.POST.get("city")
            user.state = request.POST.get("state")
            user.zip = request.POST.get("zip")
            user.set_password(request.POST.get("password"))
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('/auth_app/login') 
        else:
            messages.error(request, msg)
            return render(request, self.template_name, {'form_data': request.POST})



class LoginView(TemplateView):
    template_name = 'auth_app/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        # If authentication is
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('/auth_app/dashboard') 
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, self.template_name, {'email': email})




@method_decorator(login_required(login_url='/auth_app/login'), name='dispatch')
class DashboardView(TemplateView):
    template_name = 'auth_app/dashboard.html'


def logout_view(request):
    logout(request)
    return redirect('/auth_app/login')


