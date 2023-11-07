from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from calender.models import Events

# def index(request):
#     # 사용자가 로그인했는지 확인합니다.
#     if request.user.is_authenticated:
#         # 로그인한 사용자의 이벤트만 필터링합니다.
#         user_events = Events.objects.filter(user=request.user)
#     else:
#         # 비로그인 사용자에게는 이벤트를 보여주지 않습니다.
#         user_events = Events.objects.none()
#
#     context = {
#         "events": user_events,
#     }
#     return render(request, 'calendar.html', context)

@login_required(login_url='accounts/login/')  # 로그인하지 않은 사용자를 로그인 페이지로 리다이렉트합니다.
def index(request):
    # 현재 로그인한 사용자와 연결된 이벤트들만 가져옵니다.
    user_events = Events.objects.filter(user=request.user)

    context = {
        "events": user_events,
    }
    return render(request, 'calendar.html', context)


@login_required(login_url='accounts/login/')
def all_events(request):
    # 현재 로그인한 사용자와 연결된 이벤트들만 가져옵니다.
    user_events = Events.objects.filter(user=request.user)
    out = []
    for event in user_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%Y-%m-%d %H:%M:%S"),
            'end': event.end.strftime("%Y-%m-%d %H:%M:%S"),
            'user_id': event.user.id  # 로그인한 사용자의 ID를 넣어줍니다.
        })

    return JsonResponse(out, safe=False)


@login_required
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)

    event = Events(name=str(title), start=start, end=end, user=request.user)
    event.save()

    data = {}
    return JsonResponse(data)


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
