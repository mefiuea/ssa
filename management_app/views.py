from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .forms import EventsForm, ProfileEditForm
from .models import Events, Profile


@login_required(login_url='users_app:login_view')
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


@login_required(login_url='users_app:login_view')
def profile_view(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        user = User.objects.get(username=request.user)
        try:
            profile_instance = Profile.objects.get(owner=user.id)
        except:
            # create default profile for user if not exist
            profile_instance = Profile.objects.create(owner=user)

        return render(request, 'management_app/profile.html', context={
            'user': user,
            'profile_instance': profile_instance
        })


@login_required(login_url='users_app:login_view')
def profile_edit_view(request, user_id):
    if request.method == 'POST':
        instance = get_object_or_404(Profile, owner=user_id)
        form = ProfileEditForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return redirect(reverse_lazy('management_app:profile_view'))
    else:
        instance = get_object_or_404(Profile, owner=user_id)
        form = ProfileEditForm(initial={
            'nick_name': instance.nick_name,
            'lead_replica': instance.lead_replica,
            'additional_replica': instance.additional_replica,
            'side_replica': instance.side_replica,
            'best_place': instance.best_place,
            'gear': instance.gear
        })
    return render(request, 'management_app/profile_edit.html', context={'form': form})


@login_required(login_url='users_app:login_view')
def event_add_view(request):
    if request.method == 'POST':
        form = EventsForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return redirect(reverse_lazy('management_app:profile_view'))
        else:
            # TODO: obsłużyć błędy walidacji
            print('Problem')
            return redirect(reverse_lazy('management_app:profile_view'))

    if request.method == 'GET':
        form = EventsForm()
        return render(request, 'management_app/add_event.html', context={'form': form})


@login_required(login_url='users_app:login_view')
def events_view(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        events_instance = Events.objects.all().order_by('-date')
        return render(request, 'management_app/events.html', context={'events_instance': events_instance})
