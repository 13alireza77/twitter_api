# Generated by Django 3.1.5 on 2021-01-25 18:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Twitt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('video', models.FileField(blank=True, null=True, upload_to='')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occurrences', models.PositiveIntegerField(auto_created=True, default=0)),
                ('name', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^(#\\w+\\s+)+$')])),
                ('lastupdate', models.DateTimeField(default=django.utils.timezone.now)),
                ('users', models.ManyToManyField(to='twitt.Twitt')),
            ],
        ),
        migrations.CreateModel(
            name='Retwitt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('twitt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitt.twitt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'twitt')},
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('twitt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitt.twitt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'twitt')},
            },
        ),
    ]
