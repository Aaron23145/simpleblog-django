from django.views import generic
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Entry, Profile, Tag, ImportantEntry


class Index(generic.ListView):
    template_name = 'blog/content/index.html'
    context_object_name = 'latest_entries_list'

    def get_queryset(self):
        return Entry.objects.order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active_navbar'] = 'home'
        context['important_entries'] = ImportantEntry.objects.filter(
            active=True
        )
        return context


class Login(auth_views.LoginView):
    template_name = 'blog/auth/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_navbar'] = 'login'
        return context


class Signup(generic.edit.FormView):
    template_name = 'blog/auth/signup.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_navbar'] = 'signup'
        return context


def editorcp_check(user):
    if not user.is_authenticated:
        return False

    try:
        return user.profile.can_access_ecp()
    except AttributeError:
        return user.is_staff or user.is_superuser


def blog_entry(request, pk, slug):
    entry = Entry.objects.get(pk=pk)

    if entry.slug != slug:
        return redirect('blog:view_entry', pk=pk, slug=entry.slug)

    context = {
        'entry': entry,
        'important_entries': ImportantEntry.objects.filter(active=True),
    }
    return render(request, 'blog/content/entry.html', context)


class BlogTag(generic.DetailView):
    model = Tag
    template_name = 'blog/content/tag.html'


class BlogUser(generic.DetailView):
    model = User
    template_name = 'blog/content/user.html'


def blog_about(request):
    return render(request, 'blog/content/about.html', {'active_navbar': 'about'})


def blog_contact(request):
    return render(request, 'blog/content/contact.html', {'active_navbar': 'contact'})


@user_passes_test(editorcp_check)
def editorcp_index(request, success=None):
    entries = Entry.objects.all()
    tags = Tag.objects.all()
    important_entries = ImportantEntry.objects.all()
    active_important_entries = ImportantEntry.objects.filter(active=True)

    def check_no_entries_created():
        return not entries.count()

    def check_no_tags_created():
        return not tags.count()

    def check_no_important_entries_active():
        return important_entries.count() == 0 or active_important_entries.count() == 0

    alerts = {
        'no_entries_created': {
            'show': check_no_entries_created(),
            'msg': 'You have not created any entry yet. Your blog will appear without '
                   'content until you do it.',
            'type': 'danger',
        },
        'no_tags_created': {
            'show': check_no_tags_created(),
            'msg': 'You have not created any tag yet. This could provoke that your '
                   'visitors are not receiving enough description about your entries.',
            'type': 'warning',
        },
        'no_important_entries': {
            'show': check_no_important_entries_active(),
            'msg': 'You have not set any entry as important. Because of this, the carousel '
                   'of the blog pages will not appear. If you want to make it visible, mark '
                   'an entry as important.',
            'type': 'danger',
        },
    }

    success_message = {
        'entry_created': 'New entry created successfully!',
        'entry_edited': 'Existent entry edited successfully!',
        'entry_deleted': 'Entry deleted successfully!',
        'tag_created': 'New tag created successfully!',
        'tag_edited': 'Existent tag edited successfully!',
        'tag_deleted': 'Tag deleted successfully!',
        'important_entry_created': 'Entry marked as important successfully!',
        'important_entry_edited': 'Existent important entry edited sucessfully!',
        'important_entry_deleted': 'Entry marked as not important successfully!',
    }

    context = {
        'alerts': alerts,
        'success': success_message[success] if success else None
    }

    return render(request, 'blog/editorcp/index.html', context)

class EditorcpCreateEntry(UserPassesTestMixin, generic.edit.CreateView):
    model = Entry
    template_name = 'blog/editorcp/create_entry.html'
    fields = ['title', 'summary', 'content', 'tag']

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.author = self.request.user
        form.save()
        return redirect('blog:editorcp', success='entry_created')

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpListEntries(UserPassesTestMixin, generic.ListView):
    template_name = 'blog/editorcp/list_entries.html'
    context_object_name = 'latest_entries_list'

    def get_queryset(self):
        return Entry.objects.order_by('-pub_date')

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpEditEntry(UserPassesTestMixin, generic.edit.UpdateView):
    template_name = 'blog/editorcp/edit_entry.html'
    model = Entry
    fields = ['title', 'summary', 'content', 'tag']
    success_url = reverse_lazy('blog:editorcp', args=('entry_edited',))

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpDeleteEntry(UserPassesTestMixin, generic.edit.DeleteView):
    template_name = 'blog/editorcp/delete_entry.html'
    model = Entry
    success_url = reverse_lazy('blog:editorcp', args=('entry_deleted',))

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpCreateTag(UserPassesTestMixin, generic.edit.CreateView):
    model = Tag
    template_name = 'blog/editorcp/create_tag.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('blog:editorcp', args=('tag_created',))

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpListTags(UserPassesTestMixin, generic.ListView):
    template_name = 'blog/editorcp/list_tags.html'
    context_object_name = 'tag_list'

    def get_queryset(self):
        return Tag.objects.all()

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpEditTag(UserPassesTestMixin, generic.edit.UpdateView):
    template_name = 'blog/editorcp/edit_tag.html'
    model = Tag
    success_url = reverse_lazy('blog:editorcp', args=('tag_edited',))
    fields = ['name', 'description']

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpDeleteTag(UserPassesTestMixin, generic.edit.DeleteView):
    template_name = 'blog/editorcp/delete_tag.html'
    model = Tag
    success_url = reverse_lazy('blog:editorcp', args=('tag_deleted',))

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpCreateImportantEntry(UserPassesTestMixin, generic.edit.CreateView):
    template_name = 'blog/editorcp/create_important_entry.html'
    model = ImportantEntry
    fields = ['entry', 'image_name']
    success_url = reverse_lazy(
        'blog:editorcp', args=('important_entry_created',))

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpListImportantEntries(UserPassesTestMixin, generic.ListView):
    template_name = 'blog/editorcp/list_important_entries.html'
    context_object_name = 'important_entries_list'

    def get_queryset(self):
        return ImportantEntry.objects.all()

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpEditImportantEntry(UserPassesTestMixin, generic.edit.UpdateView):
    template_name = 'blog/editorcp/edit_important_entry.html'
    model = ImportantEntry
    success_url = reverse_lazy(
        'blog:editorcp', args=('important_entry_edited',))
    fields = ['entry', 'image_name', 'active']

    def test_func(self):
        return editorcp_check(self.request.user)


class EditorcpDeleteImportantEntry(UserPassesTestMixin, generic.edit.DeleteView):
    template_name = 'blog/editorcp/delete_important_entry.html'
    model = ImportantEntry
    success_url = reverse_lazy(
        'blog:editorcp',
        args=('important_entry_deleted',)
    )

    def test_func(self):
        return editorcp_check(self.request.user)
