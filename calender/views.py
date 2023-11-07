from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Events


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
            'user_id': event.user.id  # 로그인한 사용자의 ID를 넣어줍니다.
        })

    return JsonResponse(out, safe=False)

# 이벤트를 추가할 때 동작하는 함수
@login_required
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)

    event = Events(name=str(title), start=start, end=end, user=request.user)
    event.save()

    data = {}
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
