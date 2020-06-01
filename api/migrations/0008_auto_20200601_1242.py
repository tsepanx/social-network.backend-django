# Generated by Django 3.0.6 on 2020-06-01 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200601_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='from_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='api.Profile'),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='to_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='followers', to='api.Profile'),
        ),
    ]
