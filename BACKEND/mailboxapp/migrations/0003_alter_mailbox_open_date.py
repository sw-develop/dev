# Generated by Django 3.2.6 on 2021-08-22 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailboxapp', '0002_alter_mailbox_mailbox_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailbox',
            name='open_date',
            field=models.DateField(),
        ),
    ]