# Generated by Django 4.1.2 on 2022-12-19 12:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_company_datetime_history_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='datetime_new',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 19, 12, 40, 43, 327131, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='datetime_new',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 19, 12, 40, 43, 327131, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AddField(
            model_name='licenseplate',
            name='datetime_new',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 19, 12, 40, 43, 327131, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AddField(
            model_name='targetimage',
            name='datetime_new',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 19, 12, 40, 43, 327131, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
