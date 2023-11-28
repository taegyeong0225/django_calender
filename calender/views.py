from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Events


# 스크줄러
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import pytz


# 메일 전송
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

# 웹 크롤링
from bs4 import BeautifulSoup
import requests

from django.contrib import messages


def index(request):
    # 로그인한 사용자의 이벤트만 가져옵니다. 로그인하지 않았다면 모든 이벤트를 가져옵니다.
    user_events = Events.objects.filter(user=request.user) if request.user.is_authenticated else Events.objects.all()

    # 로그인 여부에 따라 템플릿에 변수 전달
    context = {
        "events": user_events,
        "is_user_authenticated": request.user.is_authenticated,
    }
    return render(request, 'calendar.html', context)


# 이벤트를 화면에 뿌려주는 함수
@login_required(login_url='accounts/login/')
def all_events(request):
    # 현재 로그인한 사용자와 연결된 이벤트들만 가져옵니다.
    user_events = Events.objects.filter(user=request.user)
    out = [] # 배열 선언
    for event in user_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%Y-%m-%d %H:%M:%S"),
            'end': event.end.strftime("%Y-%m-%d %H:%M:%S"),
            'user_id': event.user.id,  # 로그인한 사용자의 ID를 넣어줍니다.
        })

    return JsonResponse(out, safe=False)


# 웹 스크래핑을 통해 레시피 링크를 얻는 함수
def get_recipe_links(food):
    base_url = "https://search.naver.com/search.naver?where=view&sm=tab_jum&query="
    end = "+요리+레시피"
    search_url = base_url + food + end
    r = requests.get(search_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    cook_name_and_link = soup.select(".title_link._cross_trigger")
    links = []
    for e, item in enumerate(cook_name_and_link, 1):
        if e > 10:
            break
        title = item.text
        link = item.get('href')
        links.append(f'<li><a href="{link}">{title}</a></li>')
    return '<ul>' + ''.join(links) + '</ul>'


# 이메일 전송 함수
def send_email_function(email, name, date):    # 이메일 서버 연결 정보
    smtp_server = 'smtp.gmail.com'  # SMTP 서버 주소 (Gmail의 경우)
    smtp_port = 587  # SMTP 서버 포트 (Gmail의 TLS 포트), 465와의 차이는?

    date_only = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    recipe_links = get_recipe_links(name)  # 레시피 링크 가져오기

    # 이메일 메세지 설정
    subject = f' 장고 : {name}의 소비기한이 3일 남았습니다!'  # 이메일 제목
    body = f'{name}의 소비기한이 3일 남았습니다!<br>(소비기한: {date_only})<br><br>{recipe_links}'
    sender = 'sw.project.django@gmail.com'  # 발신자 이메일 주소
    # receiver = 'taegeong@naver.com'  # 수신자 이메일 주소

    # 이메일 메세지 생성
    msg = MIMEMultipart()
    msg['Subject'] = subject  # 이메일 제목 설정
    msg['From'] = sender  # 발신자 이메일 주소 설정
    msg['To'] = email  # 수신자 이메일 주소 설정
    msg.attach(MIMEText(body, 'html'))

    # 이메일 발송
    with smtplib.SMTP(smtp_server, smtp_port) as server:  # SMTP 서버 연결
        server.starttls()  # TLS(전송 계층 보안) 시작
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  # 이메일 계정 로그인
        server.send_message(msg)  # 메시지 발송


# 이메일 스케줄링 함수
def schedule_email(user_email, title, event_date):
    timezone = pytz.timezone('Asia/Seoul')
    send_date = datetime.strptime(event_date, "%Y-%m-%d %H:%M:%S") - timedelta(days=3)
    # send_date = datetime.now()
    send_date_with_tz = timezone.localize(send_date)

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_email_function,
        'date',
        run_date=send_date_with_tz,
        args=[user_email, title, event_date]
    )
    scheduler.start()


@login_required
def add_event(request):
    # 요청으로부터 데이터 가져오기
    title = request.GET.get("title", None)
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    f_category = request.GET.get("f_category", None)  # f_category 값 가져오기

    # 새로운 이벤트 객체 생성 및 저장
    event = Events(
        name=str(title),
        start=start,
        end=end,
        f_category=f_category,  # 카테고리 설정
        user=request.user
    )
    event.save()

    # 사용자 이메일과 이벤트 날짜 가져오기
    user_email = request.user.email
    event_date = start


    # 이메일 스케줄링
    schedule_email(user_email, title, event_date)

    # JSON 응답 반환
    data = {'id': event.id}  # 생성된 이벤트의 ID를 응답 데이터에 포함
    return JsonResponse(data)

# 이벤트를 수정할 때 동작하는 함수
@login_required
def update(request):
    event_id = request.GET.get("id", None)
    event = get_object_or_404(Events, id=event_id)

    # 현재 사용자가 이벤트 소유자인지 또는 관리자인지 확인
    if event.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("이 이벤트를 수정할 권한이 없습니다.")

    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)

    event.start = start
    event.end = end
    event.name = title
    event.save()

    data = {"status": "success"}
    return JsonResponse(data)

# 이벤트를 삭제할 때 동작하는 함수
@login_required
def remove(request):
    event_id = request.GET.get("id", None)
    event = get_object_or_404(Events, id=event_id)

    # 현재 사용자가 이벤트 소유자인지 또는 관리자인지 확인
    if event.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("이 이벤트를 삭제할 권한이 없습니다.")

    event.delete()

    data = {"status": "success"}
    return JsonResponse(data)


# 카테고리별 이벤트를 필터링하는 뷰
@login_required
def get_category_events(request, category):
    if category not in ['food', 'no-food']:
        return JsonResponse({'error': 'Invalid category'}, status=400)

    category_events = Events.objects.filter(user=request.user, f_category=category)
    data = [{
        'title': event.name,
        'id': event.id,
        'start': event.start.strftime("%Y-%m-%d %H:%M:%S"),
        'end': event.end.strftime("%Y-%m-%d %H:%M:%S"),
    } for event in category_events]

    return JsonResponse(data, safe=False)


