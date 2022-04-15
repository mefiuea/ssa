from django.core.exceptions import ValidationError
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
        form = ProfileEditForm(instance=instance)
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
            # raise ValidationError("problem z walidacja!")
            return redirect(reverse_lazy('management_app:profile_view'))

    if request.method == 'GET':
        form = EventsForm()
        return render(request, 'management_app/add_event.html', context={'form': form})


# @login_required(login_url='users_app:login_view')
def events_view(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        events_instance = Events.objects.all().order_by('-date')
        return render(request, 'management_app/events.html', context={'events_instance': events_instance})


@login_required(login_url='users_app:login_view')
def event_detailed_view(request, event_id):
    if request.method == 'POST':
        if 'participate_in_button' in request.POST:
            concerned_user_instance = request.user
            event_instance = Events.objects.get(pk=event_id)
            # add user to event
            event_instance.participants.add(concerned_user_instance)
            return redirect('management_app:event_detailed_view', event_id)

        if 'cancel_participation_button' in request.POST:
            concerned_user_instance = request.user
            event_instance = Events.objects.get(pk=event_id)
            # remove user from event
            event_instance.participants.remove(concerned_user_instance)
            return redirect('management_app:event_detailed_view', event_id)

    if request.method == 'GET':
        creator_instance = request.user
        event_instance = Events.objects.get(pk=event_id)
        participants = event_instance.participants.all()
        participants_list = []
        for participant in participants:
            participants_list.append(participant.username)

        # check if the logged-in user already take part in event
        if creator_instance in participants:
            creator_already_take_part_in_event = True
        else:
            creator_already_take_part_in_event = False

        # check if the logged-in user is the creator of the event
        if creator_instance == event_instance.owner:
            is_creator = True
        else:
            is_creator = False
        return render(request, 'management_app/event_detailed_view.html', context={'event': event_instance,
                                                                                   'participants': participants_list,
                                                                                   'is_creator': is_creator,
                                                                                   'creator_already_take_part_in_event': creator_already_take_part_in_event})


@login_required(login_url='users_app:login_view')
def event_edit_view(request, event_id):
    if request.method == 'POST':
        event_instance = Events.objects.get(pk=event_id)
        form = EventsForm(request.POST, request.FILES, instance=event_instance)
        if form.is_valid():
            form.save()
            return redirect('management_app:event_detailed_view', event_id)

    if request.method == 'GET':
        event_instance = Events.objects.get(pk=event_id)
        form = EventsForm(instance=event_instance)
        return render(request, 'management_app/event_edit_view.html', context={'form': form,
                                                                               'event_instance': event_instance})


@login_required(login_url='users_app:login_view')
def event_delete_view(request, event_id):
    if request.method == 'POST':
        event_instance = Events.objects.get(pk=event_id)
        event_instance.delete()
        return redirect(reverse_lazy('management_app:events_view'))

    if request.method == 'GET':
        event_instance = Events.objects.get(pk=event_id)
        return render(request, 'management_app/event_delete_view.html', context={'event_instance': event_instance})
