from django.shortcuts import render

# 필요한 모듈 임포트
from django.http import JsonResponse

from django.shortcuts import render
from .models import Events # 'calender' 앱의 'models.py'에서 'Events' 모델을 임포트
from django.contrib.auth.decorators import login_required # login 확인


def user_events_view(request):
    if request.user.is_authenticated:
        user_events = Events.objects.filter(user=request.user)
        return render(request, 'landing.html', {'events': user_events})
    else:
        # 사용자가 로그인하지 않았을 경우 처리
        return render(request, 'landing.html')

# 캘린더에 이벤트 정보를 제공하는 뷰
def all_events(request):
    if request.user.is_authenticated:  # 사용자가 인증되었는지 확인
        user_events = Events.objects.filter(user=request.user)  # 현재 사용자의 이벤트만 가져옴
        out = []  # 응답으로 보낼 리스트 초기화
        for event in user_events:
            if event.end:  # 이벤트 종료 시간이 설정되어 있을 경우만 처리
                out.append({
                    'title': event.name,  # 이벤트 이름
                    'id': event.id,       # 이벤트 ID
                    'end': event.end.strftime("%m/%d/%Y %H:%M:%S"),  # 이벤트 종료 시간을 문자열로 변환
                })
        return JsonResponse(out, safe=False)  # JSON 형태로 변환하여 응답
    else:
        # 사용자가 인증되지 않았을 경우 처리
        return JsonResponse({'error': 'User not authenticated'}, status=400)


# 새로운 이벤트를 추가하는 뷰
@login_required  # 로그인한 사용자만 접근할 수 있도록 함
def add_event(request):
    if request.method == 'GET':
        end = request.GET.get("end", None)              # 요청에서 'end' 매개변수 값을 가져옴
        title = request.GET.get("title", None)          # 요청에서 'title' 매개변수 값을 가져옴
        user = request.user                             # 현재 로그인한 사용자를 가져옴
        event = Events(name=str(title), end=end, user=user)  # 새로운 이벤트 객체 생성, 현재 사용자를 포함
        event.save()                                    # 이벤트를 DB에 저장
        data = {'status': 'success'}                    # 응답 데이터에 성공 상태 추가
        return JsonResponse(data)                       # JSON 응답 반환
    else:
        return JsonResponse({'status': 'invalid request'}, status=400)  # 잘못된 요청에 대한 응답

# 기존 이벤트를 업데이트하는 뷰
def update(request):
    # start = request.GET.get("start", None) # 'start' 매개변수는 사용하지 않음
    end = request.GET.get("end", None)      # 요청에서 'end' 매개변수 값을 가져옴
    title = request.GET.get("title", None)  # 요청에서 'title' 매개변수 값을 가져옴
    id = request.GET.get("id", None)        # 요청에서 'id' 매개변수 값을 가져옴
    event = Events.objects.get(id=id)       # 해당 ID를 가진 이벤트 객체를 DB에서 가져옴
    # start = start                         # 'start' 값을 업데이트 (현재는 주석 처리됨)
    event.end = end                         # 'end' 값을 업데이트
    event.name = title                      # 'title' 값을 업데이트
    event.save()                            # 변경 사항을 DB에 저장
    data = {}                               # 응답 데이터 초기화
    return JsonResponse(data)               # 빈 JSON 응답 반환

# 이벤트를 삭제하는 뷰
def remove(request):
    id = request.GET.get("id", None)        # 요청에서 'id' 매개변수 값을 가져옴
    event = Events.objects.get(id=id)       # 해당 ID를 가진 이벤트 객체를 DB에서 가져옴
    event.delete()                          # 이벤트를 DB에서 삭제
    data = {}                               # 응답 데이터 초기화
    return JsonResponse(data)               # 빈 JSON 응답 반환


