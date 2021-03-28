# Generated by Django 3.0 on 2021-01-16 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_profile_birth_date'),
        ('posts', '0002_auto_20210115_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='profiles.Profile'),
        ),
    ]
