# Generated by Django 2.1.7 on 2020-03-06 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200306_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='reviewer',
            new_name='reviewed',
        ),
    ]