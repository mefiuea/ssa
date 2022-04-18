from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from management_app.models import Events, Post, Profile


def home_page_view(request):
    if request.method == 'POST':
        pass

    if request.method == 'GET':
        events_instance = Events.objects.all().order_by('-date')
        event0 = events_instance[0]
        event1 = events_instance[1]
        event2 = events_instance[2]

        posts_instance = Post.objects.all().order_by('-created_date')
        current_user_profile_instance = Profile.objects.get(owner=request.user)
        # setting Pagination
        paginator_instance = Paginator(posts_instance, 12)
        page = request.GET.get('page')
        posts_list = paginator_instance.get_page(page)
        nums = 'i' * posts_list.paginator.num_pages

        return render(request, 'home_page_app/home.html', context={'event0': event0,
                                                                   'event1': event1,
                                                                   'event2': event2,
                                                                   'posts_instance': posts_instance,
                                                                   'posts_list_paginator': posts_list,
                                                                   'nums': nums,
                                                                   'user_profile': current_user_profile_instance,
                                                                   })
