from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """Tag or keyword that will be added to an entry to describe it."""
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}: {self.description[:10]}...'


class Entry(models.Model):
    """Any entry of the blog."""
    title = models.CharField(max_length=30)
    content = models.TextField()
    summary = models.TextField()
    pub_date = models.DateTimeField('date published')
    tag = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} by {self.author}: {self.summary[:10]}'

    class Meta:
        verbose_name_plural = 'entries'


class Profile(models.Model):
    """Profile that will have extra info about the user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_editor = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} is ' + ('not ' if not self.is_editor else '') + 'an editor'

    def can_access_ecp(self):
        return self.user.is_staff or self.user.is_superuser or self.is_editor
