# Generated by Django 3.1.1 on 2020-10-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20201001_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='province',
            field=models.CharField(default='ON', max_length=2),
        ),
    ]