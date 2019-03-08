from django.views import generic
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse_lazy

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


class EditorcpCreateEntry(UserPassesTestMixin, generic.edit.CreateView):
    model = Entry
    template_name = 'blog/editorcp/create_entry.html'
    fields = ['title', 'summary', 'content', 'tag']
    login_url = 'blog:index'
    redirect_field_name = None

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.pub_date = timezone.now()
        entry.author = self.request.user
        entry.save()
        form.save_m2m()
        return redirect('blog:editorcp')

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpListEntries(UserPassesTestMixin, generic.ListView):
    template_name = 'blog/editorcp/list_entries.html'
    context_object_name = 'latest_entries_list'
    login_url = 'blog:index'
    redirect_field_name = None

    def get_queryset(self):
        return Entry.objects.order_by('-pub_date')

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpEditEntry(UserPassesTestMixin, generic.edit.UpdateView):
    template_name = 'blog/editorcp/edit_entry.html'
    model = Entry
    success_url = reverse_lazy('blog:editorcp')
    fields = ['title', 'summary', 'content', 'tag']
    login_url = 'blog:index'
    redirect_field_name = None

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpDeleteEntry(UserPassesTestMixin, generic.edit.DeleteView):
    template_name = 'blog/editorcp/delete_entry.html'
    model = Entry
    success_url = reverse_lazy('blog:editorcp')
    login_url = 'blog:index'
    redirect_field_name = None

    def test_func(self):
        return editorcp_check(self.request.user)
