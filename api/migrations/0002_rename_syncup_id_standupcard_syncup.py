# Generated by Django 4.2.1 on 2023-06-01 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standupcard',
            old_name='syncup_id',
            new_name='syncup',
        ),
    ]
