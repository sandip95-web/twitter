# Generated by Django 4.2.3 on 2023-07-18 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0006_tweet_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='github_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_bio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
