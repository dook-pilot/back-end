# Generated by Django 4.1.2 on 2022-11-24 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targetimage',
            name='image',
            field=models.FileField(upload_to='media/a84090a2-7275-40ca-87c3-7b245d2cca00.jpg'),
        ),
    ]
