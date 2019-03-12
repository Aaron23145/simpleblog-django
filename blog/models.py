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
    title = models.CharField(max_length=50)
    content = models.TextField()
    summary = models.TextField(
        help_text='A very short summary that will help your visitors to understand about what '
                  'the article is. This text will appear below your entry title and on the '
                  'carousel if it is marked as important.'
    )
    pub_date = models.DateTimeField('date published')
    tag = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()

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


class ImportantEntry(models.Model):
    """Important entries that will be displayed in the carousel."""
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    image_name = models.CharField(
        max_length=50,
        help_text='The direction and name of the image located in '
                  'the static/blog/images folder of the blog app.'
    )
    active = models.BooleanField(
        default=True,
        help_text='Whether the entry will be displayed in the '
                  'carousel or it will be hidden until you active it.'
    )

    def get_image_url(self):
        return f'blog/images/{self.image_name}'

    class Meta:
        verbose_name_plural = 'important entries'
