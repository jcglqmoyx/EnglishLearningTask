# Generated by Django 4.0.6 on 2022-08-01 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='enter_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='task.group'),
        ),
    ]
