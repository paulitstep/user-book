# Generated by Django 2.2.4 on 2019-08-27 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_book', '0007_auto_20190827_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='description',
        ),
    ]
