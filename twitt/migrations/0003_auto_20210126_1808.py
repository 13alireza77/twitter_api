# Generated by Django 3.1.5 on 2021-01-26 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitt', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
