# Generated by Django 3.0.8 on 2020-07-10 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200710_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlist',
            name='all_bids',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.Bid'),
        ),
    ]
