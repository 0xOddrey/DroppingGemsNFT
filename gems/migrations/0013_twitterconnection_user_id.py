# Generated by Django 3.2.10 on 2022-02-08 00:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gems', '0012_twittertoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterconnection',
            name='user_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
