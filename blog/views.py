from django.views import generic
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import Entry, Profile


class Index(generic.ListView):
    template_name = 'blog/content/index.html'
    context_object_name = 'latest_entries_list'

    def get_queryset(self):
        return Entry.objects.order_by('-pub_date')


class Signup(generic.edit.FormView):
    template_name = 'blog/auth/signup.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect('blog:index')


def editorcp_check(user):
    return user.is_authenticated and user.profile.can_access_ecp()


@user_passes_test(editorcp_check, login_url='blog:index', redirect_field_name=None)
def editorcp_index(request):
    return render(request, 'blog/editorcp/index.html')


@user_passes_test(editorcp_check, login_url='blog:index', redirect_field_name=None)
def editorcp_create_entry(request):
    return render(request, 'blog/editorcp/create_entry.html')
