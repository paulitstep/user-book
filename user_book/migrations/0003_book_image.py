# Generated by Django 2.2.4 on 2019-08-24 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_book', '0002_book_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='books/'),
        ),
    ]
