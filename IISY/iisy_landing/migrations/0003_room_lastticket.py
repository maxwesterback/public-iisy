# Generated by Django 2.2.7 on 2020-03-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iisy_landing', '0002_auto_20200309_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='lastTicket',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
