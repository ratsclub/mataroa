# Generated by Django 3.0.7 on 2020-06-06 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_user_cname"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user", old_name="cname", new_name="custom_domain",
        ),
    ]
