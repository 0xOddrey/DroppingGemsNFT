# Generated by Django 3.2.10 on 2022-02-11 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gems', '0016_alter_gemsmeta_is_anon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gemsmeta',
            name='image_file',
            field=models.FileField(blank=True, null=True, upload_to='gems/'),
        ),
    ]
