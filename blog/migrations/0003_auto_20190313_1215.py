# Generated by Django 2.1.7 on 2019-03-13 11:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_importantentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='summary',
            field=models.TextField(help_text='A very short summary that will help your visitors to understand about what the article is. This text will appear below your entry title and on the carousel if it is marked as important.'),
        ),
        migrations.AlterField(
            model_name='importantentry',
            name='active',
            field=models.BooleanField(default=True, help_text='Whether the entry will be displayed in the carousel or it will be hidden until you active it.'),
        ),
        migrations.AlterField(
            model_name='importantentry',
            name='image_name',
            field=models.CharField(help_text='The direction and name of the image located in the static/blog/images folder of the blog app.', max_length=50),
        ),
    ]
