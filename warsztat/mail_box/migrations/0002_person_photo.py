# Generated by Django 2.0.3 on 2018-09-10 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_box', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='photo',
            field=models.ImageField(blank=True, upload_to='mail_box/photos'),
        ),
    ]
