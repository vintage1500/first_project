# Generated by Django 4.1.7 on 2023-04-04 12:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_app', '0008_rename_bookcommentform_bookcountform'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookCountForm',
            new_name='BookCountViews',
        ),
    ]