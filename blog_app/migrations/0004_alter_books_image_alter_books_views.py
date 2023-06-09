# Generated by Django 4.1.7 on 2023-03-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_books_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='books',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Количество просмотров'),
        ),
    ]
