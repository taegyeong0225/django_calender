from django.shortcuts import render

# Create your views here.
from calender.models import Events
from django.http import JsonResponse

def index(request):
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request, 'landing.html', context)

def all_events(request):
    all_events = Events.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y", "%H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y", "%H:%M:%S"),
        })
        return JsonResponse(out, safe=False)