from django.views import generic

from .models import Entry

class Index(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_entries_list'

    def get_queryset(self):
        return Entry.objects.order_by('-pub_date')
