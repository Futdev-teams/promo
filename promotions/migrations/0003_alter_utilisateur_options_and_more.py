# Generated by Django 5.1.7 on 2025-03-26 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0002_alter_utilisateur_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='utilisateur',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='password_reset_required',
            field=models.BooleanField(default=True),
        ),
    ]
