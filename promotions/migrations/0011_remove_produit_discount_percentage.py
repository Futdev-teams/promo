# Generated by Django 5.1.7 on 2025-05-06 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0010_produit_discount_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='discount_percentage',
        ),
    ]
