# Generated by Django 3.0.8 on 2020-07-14 07:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20200714_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlist',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
