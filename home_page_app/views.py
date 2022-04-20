from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from management_app.models import Events, Post, Profile, Comment
from custom.random_string import get_random_string
from management_app.forms import CommentForm


def home_page_view(request):
    if request.method == 'POST':
        pass
        # if 'thread' in request.POST:
        #     current_user_instance = request.user
        #     # # get id of current post when clicking like button
        #     like_post_id = int(request.POST.get('like'))
        #     # # creating current post instance
        #     post_instance = Post.objects.get(pk=int(like_post_id))
        #     # # add user to current post (likes)
        #     post_instance.likes.add(current_user_instance)
        #
        #     # # check if the logged-in user already hit like button
        #     # likes = post_instance.likes.all()
        #     # if current_user_instance in likes:
        #     #     # print('True')
        #     #     messages.add_message(request, messages.INFO, True)
        #     # else:
        #     #     # print('False')
        #     #     messages.add_message(request, messages.INFO, False)
        #     return render(request, 'home_page_app/thread.html')

    if request.method == 'GET':

        events_instance = Events.objects.all().order_by('-date')
        event0 = events_instance[0]
        event1 = events_instance[1]
        event2 = events_instance[2]

        # get all posts from database ordered by data
        posts_instance = Post.objects.all().order_by('-created_date')

        # empty list to store all profiles connected with current post
        profiles_users_list = []
        for pi in posts_instance:
            profile_user_instance = Profile.objects.get(owner=pi.owner)
            profiles_users_list.append(profile_user_instance)

        # generate random string for templates for unique collapse id (only letters)
        unique_id_list = []
        for _ in range(len(profiles_users_list)):
            unique_id_list.append(get_random_string(8))

        # combination of two instances: the post and the corresponding profile (the creator of the post)
        posts_profiles_unique = zip(posts_instance, profiles_users_list, unique_id_list)

        # current_user_profile_instance = Profile.objects.get(owner=request.user)

        # setting Pagination
        paginator_instance = Paginator(posts_instance, 12)
        page = request.GET.get('page')
        posts_list = paginator_instance.get_page(page)
        nums = 'i' * posts_list.paginator.num_pages

        context_message = None
        storage = get_messages(request)
        for message in storage:
            context_message = bool(message)

        return render(request, 'home_page_app/home.html', context={'event0': event0,
                                                                   'event1': event1,
                                                                   'event2': event2,
                                                                   'posts_instance': posts_instance,
                                                                   'posts_list_paginator': posts_list,
                                                                   'nums': nums,
                                                                   'posts_and_profiles_and_unique': posts_profiles_unique,
                                                                   })


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

        return redirect('home_page_app:thread_view', post_id)

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
        # connecting two lists
        comments_profiles_list = zip(comments, profiles_commentators_list)
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

        return render(request, 'home_page_app/thread.html', context={'posts_instance': post_instance,
                                                                     'form': form,
                                                                     'profile_owner_instance': profile_owner_instance,
                                                                     'profile_commenter_instance': profile_commenter_instance,
                                                                     'comments_profiles_list': comments_profiles_list,
                                                                     'logged_user_already_liked': logged_user_already_liked,
                                                                     'logged_user_is_creator_of_post': logged_user_is_creator_of_post})
