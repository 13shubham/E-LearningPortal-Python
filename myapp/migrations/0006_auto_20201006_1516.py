# Generated by Django 3.1.1 on 2020-10-06 19:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20201001_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='address',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.RemoveField(
            model_name='order',
            name='courses',
        ),
        migrations.AddField(
            model_name='order',
            name='courses',
            field=models.ManyToManyField(to='myapp.Course'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='topic',
            name='length',
            field=models.IntegerField(blank=True, default=12, null=True),
        ),
    ]