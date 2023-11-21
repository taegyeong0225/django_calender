from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Events

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from django.conf import settings

import smtplib
from email.mime.text import MIMEText

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

# 이메일 전송 함수
def send_email_function(email, name, date):    # 이메일 서버 연결 정보
    smtp_server = 'smtp.gmail.com'  # SMTP 서버 주소 (Gmail의 경우)
    smtp_port = 587  # SMTP 서버 포트 (Gmail의 TLS 포트), 465와의 차이는?

    # 이메일 메세지 설정
    subject = f' 장고 : {name}의 소비기한이 3일 남았습니다!'  # 이메일 제목
    body = f'{name}의 소비기한이 3일 남았습니다!  (소비기한: {date}) +++ [웹크롤링 음식명 내용]'  # 이메일 본문 내용
    sender = 'sw.project.django@gmail.com'  # 발신자 이메일 주소
    # receiver = 'taegeong@naver.com'  # 수신자 이메일 주소

    # 이메일 메세지 생성
    msg = MIMEText(body)  # 이메일 본문을 MIMEText 객체로 생성
    msg['Subject'] = subject  # 이메일 제목 설정
    msg['From'] = sender  # 발신자 이메일 주소 설정
    msg['To'] = email  # 수신자 이메일 주소 설정

    # 이메일 발송
    with smtplib.SMTP(smtp_server, smtp_port) as server:  # SMTP 서버 연결
        server.starttls()  # TLS(전송 계층 보안) 시작
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  # 이메일 계정 로그인
        server.send_message(msg)  # 메시지 발송


# 이메일 스케줄링 함수
def schedule_email(user_email, title, event_date):
    # 날짜 3일 전 계산
    # send_date = datetime.strptime(event_date, "%Y-%m-%d") - timedelta(days=3)
    # 'YYYY-MM-DD HH:MM:SS' 형식으로 날짜와 시간 모두를 해석
    send_date = datetime.strptime(event_date, "%Y-%m-%d %H:%M:%S") - timedelta(days=3)

    timezone = pytz.timezone('Asia/Seoul')

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_email_function,
        'date',
        run_date=send_date.replace(tzinfo=timezone),
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
    event_date = start.split('T')[0]  # 'YYYY-MM-DD' 형식으로 변환

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

