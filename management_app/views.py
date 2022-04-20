from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from .forms import EventsForm, ProfileEditForm, OffersForm, PostForm, CommentForm
from .models import Events, Profile, Offers, Post, Comment
from custom.random_string import get_random_string


@login_required(login_url='users_app:login_view')
def profile_view(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        user = User.objects.get(username=request.user)
        profile_instance = Profile.objects.get(owner=user.id)

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

        # setting Pagination
        paginator_instance = Paginator(events_instance, 12)
        page = request.GET.get('page')
        events_list = paginator_instance.get_page(page)
        nums = 'i' * events_list.paginator.num_pages

        return render(request, 'management_app/events.html', context={'events_instance': events_instance,
                                                                      'events_list_paginator': events_list,
                                                                      'nums': nums})


@login_required(login_url='users_app:login_view')
def event_detailed_view(request, event_id):
    if request.method == 'POST':
        if 'participate_in_button' in request.POST:
            concerned_user_instance = request.user
            event_instance = Events.objects.get(pk=event_id)
            # add user to event
            event_instance.participants.add(concerned_user_instance)

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

        # check if logged-in user is the creator of the event
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


@login_required(login_url='users_app:login_view')
def persons_view(request):
    if request.method == 'POST':
        pass

    if request.method == 'GET':
        profiles_users_instance = Profile.objects.all().order_by('owner').select_related('owner')

        # generate random string for templates for unique collapse id (only letters)
        unique_id_list = []
        for _ in range(profiles_users_instance.count()):
            unique_id_list.append(get_random_string(8))

        # setting Pagination
        paginator_instance = Paginator(profiles_users_instance, 12)
        page = request.GET.get('page')
        profiles_users_instance_pagination = paginator_instance.get_page(page)
        nums = 'i' * profiles_users_instance_pagination.paginator.num_pages

        # connect to lists
        pagination_unique_list = zip(profiles_users_instance_pagination, unique_id_list)

        return render(request, 'management_app/persons.html', context={
            'profiles_users_instance': profiles_users_instance_pagination,
            'pagination_unique_list': pagination_unique_list,
            'nums': nums})


@login_required(login_url='users_app:login_view')
def offer_add_view(request):
    if request.method == 'POST':
        form = OffersForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return redirect(reverse_lazy('management_app:profile_view'))
        else:
            # errors = form.errors
            # TODO: obsłużyć błędy walidacji
            raise ValidationError("problem z walidacja!")

    if request.method == 'GET':
        form = OffersForm()
        return render(request, 'management_app/add_offer.html', context={'form': form})


@login_required(login_url='users_app:login_view')
def market_view(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        offers_instance = Offers.objects.all().order_by('-created_date')

        # setting Pagination
        paginator_instance = Paginator(offers_instance, 12)
        page = request.GET.get('page')
        offers_list = paginator_instance.get_page(page)
        nums = 'i' * offers_list.paginator.num_pages

        return render(request, 'management_app/market.html', context={'offers_instance': offers_instance,
                                                                      'offers_list_paginator': offers_list,
                                                                      'nums': nums})


@login_required(login_url='users_app:login_view')
def offer_detailed_view(request, offer_id):
    if request.method == 'POST':
        pass

    if request.method == 'GET':
        creator_instance = request.user
        offer_instance = Offers.objects.get(pk=offer_id)

        # check if the logged-in user is the creator of the offer
        if creator_instance == offer_instance.owner:
            is_creator = True
        else:
            is_creator = False
        return render(request, 'management_app/offer_detailed_view.html', context={'offer': offer_instance,
                                                                                   'is_creator': is_creator})


@login_required(login_url='users_app:login_view')
def offer_edit_view(request, offer_id):
    if request.method == 'POST':
        offer_instance = Offers.objects.get(pk=offer_id)
        form = OffersForm(request.POST, request.FILES, instance=offer_instance)
        if form.is_valid():
            form.save()
            return redirect('management_app:offer_detailed_view', offer_id)
        else:
            print(form.errors)

    if request.method == 'GET':
        offer_instance = Offers.objects.get(pk=offer_id)
        form = OffersForm(instance=offer_instance)
        return render(request, 'management_app/offer_edit_view.html', context={'form': form,
                                                                               'offer_instance': offer_instance})


@login_required(login_url='users_app:login_view')
def offer_delete_view(request, offer_id):
    if request.method == 'POST':
        offer_instance = Offers.objects.get(pk=offer_id)
        offer_instance.delete()
        return redirect(reverse_lazy('management_app:market_view'))

    if request.method == 'GET':
        offer_instance = Offers.objects.get(pk=offer_id)
        return render(request, 'management_app/offer_delete_view.html', context={'offer_instance': offer_instance})


@login_required(login_url='users_app:login_view')
def post_add_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return redirect(reverse_lazy('home_page_app:home_view'))
        else:
            # errors = form.errors
            # TODO: obsłużyć błędy walidacji
            raise ValidationError("problem z walidacja!")

    if request.method == 'GET':
        form = PostForm()
        return render(request, 'management_app/add_post.html', context={'form': form})


@login_required(login_url='users_app:login_view')
def thread_view(request, post_id):
    if request.method == 'POST':
        current_user_instance = request.user
        # creating current post instance
        post_instance = Post.objects.get(pk=post_id)

        if 'add_comment_button' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                form.instance.owner = current_user_instance
                form.instance.post = post_instance
                form.save()

        if 'like_button' in request.POST:
            # add logged user to post instance (many to many field)
            post_instance.likes.add(current_user_instance)

        if 'unlike_button' in request.POST:
            # remove logged user to post instance (many to many field)
            post_instance.likes.remove(current_user_instance)

        return redirect('management_app:thread_view', post_id)

    if request.method == 'GET':
        current_user_instance = request.user
        # get specific post from database
        post_instance = Post.objects.get(pk=post_id)
        # get profile of owner of this specific post
        profile_owner_instance = Profile.objects.get(owner=post_instance.owner)
        # get profile of current comment user (logged user)
        profile_commenter_instance = Profile.objects.get(owner=request.user)
        # get comments to this specific post
        comments = Comment.objects.filter(post=post_instance).order_by('-created_date')
        # get profiles of all commentators (persons who post comment)
        profiles_commentators_list = []
        for comment in comments:
            profile_commentator_instance = Profile.objects.get(owner=comment.owner)
            profiles_commentators_list.append(profile_commentator_instance)

        # setting Pagination
        paginator_instance = Paginator(comments, 6)
        page = request.GET.get('page')
        comments_instance_paginator = paginator_instance.get_page(page)
        nums = 'i' * comments_instance_paginator.paginator.num_pages

        # connecting two lists
        comments_profiles_list = zip(comments_instance_paginator, profiles_commentators_list)
        # generate form
        form = CommentForm()

        # check status like/unlike buttons to current user
        likes = post_instance.likes.all()
        if current_user_instance in likes:
            logged_user_already_liked = True
        else:
            logged_user_already_liked = False

        # check status if logged user is creator of post
        if post_instance.owner == current_user_instance:
            logged_user_is_creator_of_post = True
        else:
            logged_user_is_creator_of_post = False

        return render(request, 'management_app/thread.html', context={'posts_instance': post_instance,
                                                                      'form': form,
                                                                      'profile_owner_instance': profile_owner_instance,
                                                                      'profile_commenter_instance': profile_commenter_instance,
                                                                      'comments_profiles_list': comments_profiles_list,
                                                                      'logged_user_already_liked': logged_user_already_liked,
                                                                      'logged_user_is_creator_of_post': logged_user_is_creator_of_post,
                                                                      'comments_instance_paginator': comments_instance_paginator})


@login_required(login_url='users_app:login_view')
def post_edit_view(request, post_id):
    if request.method == 'POST':
        post_instance = Post.objects.get(pk=post_id)
        form = PostForm(request.POST, instance=post_instance)
        if form.is_valid():
            form.save()
            return redirect('management_app:thread_view', post_id)
        else:
            print('problem z walidacja')

    if request.method == 'GET':
        post_instance = Post.objects.get(pk=post_id)
        form = PostForm(instance=post_instance)
        return render(request, 'management_app/post_edit_view.html', context={'form': form,
                                                                              'post_instance': post_instance})


@login_required(login_url='users_app:login_view')
def comment_edit_view(request, post_id, comment_id):
    if request.method == 'POST':
        comment_instance = Comment.objects.get(pk=comment_id)
        form = CommentForm(request.POST, instance=comment_instance)
        if form.is_valid():
            form.save()
            return redirect('management_app:thread_view', post_id)
        else:
            print('problem z walidacja')

    if request.method == 'GET':
        comment_instance = Comment.objects.get(pk=comment_id)
        form = CommentForm(instance=comment_instance)
        return render(request, 'management_app/comment_edit_view.html', context={'form': form,
                                                                                 'comment_instance': comment_instance,
                                                                                 'post_id': post_id})
