# Generated by Django 3.0.7 on 2020-06-13 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0028_auto_20200610_2248"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="footer_note",
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
