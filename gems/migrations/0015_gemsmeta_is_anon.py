# Generated by Django 3.2.10 on 2022-02-10 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gems', '0014_gemsmeta_background'),
    ]

    operations = [
        migrations.AddField(
            model_name='gemsmeta',
            name='is_anon',
            field=models.BooleanField(default=False),
        ),
    ]