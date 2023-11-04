from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from calender.models import Events

def index(request):
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request, 'landing.html', context)

'''
def all_events(request):
    all_events = Events.objects.all() # 모든 이벤트 받아옴
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y" "%H:%M:%S"),
        })
    return JsonResponse(out, safe=False) # 클라이언트한테 전달
'''
def all_events(request):
    all_events = Events.objects.all()
    out = []
    for event in all_events:
        if event.start and event.end:  # start와 end가 None이 아닌 경우에만 strftime을 호출
            out.append({
                'title': event.name,
                'id': event.id,
                'start': event.start.strftime("%m/%d/%Y %H:%M:%S"),
                'end': event.end.strftime("%m/%d/%Y %H:%M:%S"),
            })
    return JsonResponse(out, safe=False)

def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
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