# Generated by Django 4.2.1 on 2023-06-17 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_standupcard_standup_card_constraint_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualcardupdate',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='individual_updates', to='api.synchronuser'),
        ),
    ]
