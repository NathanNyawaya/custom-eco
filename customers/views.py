from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from store.models import Customer
from .forms import SignUpForm


# Create your views here.

def login_user(request):
    if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('store')
            else:
                # Return an 'invalid login' error message.
                messages.success(
                    request, ("Confirm your loggins, and try again!"))
                return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
     logout(request)
     return redirect('ads')


def register_user(request):
     form = SignUpForm()
     if request.method == 'POST':
          form = SignUpForm(request.POST)
          if form.is_valid():
               form.save()
               username = form.cleaned_data['username']
               password = form.cleaned_data['password1']
               user = authenticate(username=username, password=password)
               Customer.objects.create(user=user, name=username, email=user.email)
               login(request, user)
               messages.success(request, ("Reigistered successfully"))
               return redirect("store")
          else:
            messages.success(request, ("Hey try again loggin in"))
            form = UserCreationForm()
     return render(request, 'authenticate/register.html',{'form': form})


