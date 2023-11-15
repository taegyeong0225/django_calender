from django.shortcuts import render

# accounts/views.py
# from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

'''
signup : 회원가입 
- post 방식으로 요청을 받음
- 비밀번호가 같으면 유저를 만들고 로그인 진행
'''

def signup(request):
    duplicate_username = False
    wrong_password = False

    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']

            # 중복 아이디 확인
            if User.objects.filter(username=username).exists():
                duplicate_username = True
            else:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],
                )
                auth.login(request, user)
                return redirect('/')
        else:
            wrong_password = True

    return render(request, 'signup.html',
                  {'duplicate_username': duplicate_username, 'wrong_password': wrong_password})


'''
login : 로그인
- post 방식으로 요청을 받음
- 저장된 정보와 같으면 로그인 진행
'''
# def login(request):
#     wrong_password = False
#     user_does_not_exist = False
#
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('home')
#         else:
#             user_does_not_exist = True
#
#     return render(request, 'login.html', {'wrong_password': wrong_password, 'user_does_not_exist': user_does_not_exist})


def login(request):
    user_does_not_exist = False
    wrong_password = False

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 사용자가 존재하지 않는 경우와 비밀번호가 다른 경우를 별도로 처리
        try:
            user = User.objects.get(username=username)
            if user is not None and user.check_password(password):
                auth.login(request, user)
                return redirect('home') # 로그인 후 홈화면으로 이동
            else:
                wrong_password = True
        except User.DoesNotExist:
            user_does_not_exist = True

    return render(request, 'login.html', {'user_does_not_exist': user_does_not_exist, 'wrong_password': wrong_password})

# 1. 아이디가 등록되어 있는지 확인합니다.
# 1-1. 아이디가 등록되어 있지 않다면 user_does_not_exist = True
# 2. 등록되어 있다면 비밀번호가 일치하는지 확인합니다.
# 2-1. 비밀번호가 일치하지 않으면 wrong_password = True
# 조건에 맞게 수정해주세요.




'''
logout : 로그인
- logout 진행 후 home으로 이동
'''
def logout(request):
    auth.logout(request)
    return redirect('home')

'''
home이란? landing 페이지로 이동!
'''
def home(request):
    return render(request, 'landing.html')