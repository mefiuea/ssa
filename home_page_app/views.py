from django.shortcuts import render
from django.views.generic import TemplateView

from management_app.models import Events


# class HomeView(TemplateView):
#     template_name = 'home_page_app/home.html'


def home_page_view(request):
    if request.method == 'POST':
        pass

    if request.method == 'GET':
        events_instance = Events.objects.all().order_by('-date')
        event0 = events_instance[0]
        event1 = events_instance[1]
        event2 = events_instance[2]

        return render(request, 'home_page_app/home.html', context={'event0': event0,
                                                                   'event1': event1,
                                                                   'event2': event2})
