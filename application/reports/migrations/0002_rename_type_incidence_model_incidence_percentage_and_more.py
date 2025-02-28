# Generated by Django 4.2.6 on 2024-08-11 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incidence',
            old_name='type',
            new_name='model',
        ),
        migrations.AddField(
            model_name='incidence',
            name='percentage',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='incidence',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]
