# Generated by Django 4.0.5 on 2022-07-18 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoes_store', '0005_rename_full_name_customer_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='name',
            new_name='full_name',
        ),
    ]
