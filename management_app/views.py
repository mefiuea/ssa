from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import EventsForm


def event_add_view(request):
    if request.method == 'POST':
        form = EventsForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return redirect(reverse_lazy('home_page_app:home_view'))
    else:
        form = EventsForm()

    return render(request, 'management_app/add_event.html', context={'form': form})
