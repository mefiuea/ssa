from django.shortcuts import render
from django.views import View
from django.contrib.auth.forms import UserCreationForm


class Signup(View):
    def post(self, request):
        pass

    def get(self, request):
        form = UserCreationForm()
        context = {
            'form': form,
        }
        return render(request, 'users_app/signup.html', context=context)
