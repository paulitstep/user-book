# Generated by Django 2.2.4 on 2019-08-24 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_book', '0003_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_book/'),
        ),
    ]
