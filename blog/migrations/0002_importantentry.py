# Generated by Django 2.1.7 on 2019-03-12 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportantEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('entry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.Entry')),
            ],
            options={
                'verbose_name_plural': 'important entries',
            },
        ),
    ]