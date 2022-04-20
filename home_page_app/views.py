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

        # setting Pagination
        paginator_instance = Paginator(posts_instance, 3)
        page = request.GET.get('page')
        posts_instance_paginator = paginator_instance.get_page(page)
        nums = 'i' * posts_instance_paginator.paginator.num_pages

        # combination of three instances: the posts(from paginator), corresponding profile (the creator of the post) and
        # unique number for bootstrap template
        posts_profiles_unique = zip(posts_instance_paginator, profiles_users_list, unique_id_list)

        return render(request, 'home_page_app/home.html', context={'event0': event0,
                                                                   'event1': event1,
                                                                   'event2': event2,
                                                                   'posts_instance': posts_instance,
                                                                   'nums': nums,
                                                                   'posts_and_profiles_and_unique': posts_profiles_unique,
                                                                   'posts_instance_paginator': posts_instance_paginator,
                                                                   })
