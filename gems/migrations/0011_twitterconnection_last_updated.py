# Generated by Django 3.2.10 on 2022-02-06 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gems', '0010_auto_20220206_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterconnection',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
