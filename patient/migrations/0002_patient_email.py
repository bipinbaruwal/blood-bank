# Generated by Django 3.0.5 on 2021-05-03 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='email',
            field=models.EmailField(max_length=50, null=True),
        ),
    ]