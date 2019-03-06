from django.views import generic
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import Entry


class Index(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_entries_list'

    def get_queryset(self):
        return Entry.objects.order_by('-pub_date')


def signup(request):
    logout(request)

    if request.method == 'GET':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('blog:index')

    return render(request, 'blog/signup.html', {'form': form})
