from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from calender.models import Events

def index(request):
    # 사용자가 로그인했는지 확인합니다.
    if request.user.is_authenticated:
        # 로그인한 사용자의 이벤트만 필터링합니다.
        user_events = Events.objects.filter(user=request.user)
    else:
        # 비로그인 사용자에게는 이벤트를 보여주지 않습니다.
        user_events = Events.objects.none()

    context = {
        "events": user_events,
    }
    return render(request, 'calendar.html', context)



def all_events(request):
    all_events = Events.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
            'user_id': request.user.id  # 로그인한 사용자의 ID를 넣어줍니다.
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

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)