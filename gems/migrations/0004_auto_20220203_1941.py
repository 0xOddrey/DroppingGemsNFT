# Generated by Django 3.2.10 on 2022-02-03 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gems', '0003_alter_gemsmeta_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gemsmeta',
            name='svg_image',
        ),
        migrations.AlterField(
            model_name='gemsmeta',
            name='image',
            field=models.TextField(max_length=3500),
        ),
    ]