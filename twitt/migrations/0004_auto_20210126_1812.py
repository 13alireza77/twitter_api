# Generated by Django 3.1.5 on 2021-01-26 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitt', '0003_auto_20210126_1808'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hashtag',
            old_name='users',
            new_name='twitts',
        ),
    ]
