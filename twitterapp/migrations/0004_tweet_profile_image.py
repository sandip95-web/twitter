# Generated by Django 4.2.3 on 2023-07-13 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0003_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
