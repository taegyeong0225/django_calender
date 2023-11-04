from django.shortcuts import render

# accounts/views.py
from django.contrib import auth
from django.contrib.auth import authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def signup(request):
    duplicate_username = False

    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']

            # 중복 아이디 확인
            if User.objects.filter(username=username).exists():
                duplicate_username = True
            else:
                user = User.objects.create_user(
                    username=username,
                    password=request.POST['password1'],
                    email=request.POST['email'],
                )
                auth.login(request, user)
                return redirect('/')

    return render(request, 'signup.html', {'duplicate_username': duplicate_username})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def home(request):
    return render(request, 'landing.html')


# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             user = User.objects.create_user(
#                 username=request.POST['username'],
#                 password=request.POST['password1'],
#                 email=request.POST['email'],
#             )
#             auth.login(request, user)
#             return redirect('/')
#         return render(request, 'signup.html')
#     else:
#         form = UserCreationForm
#         return render(request, 'signup.html', {'form':form})