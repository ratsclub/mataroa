# Generated by Django 3.1 on 2020-08-30 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0046_auto_20200821_1820"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="custom_domain_cert",
        ),
        migrations.RemoveField(
            model_name="user",
            name="custom_domain_key",
        ),
    ]