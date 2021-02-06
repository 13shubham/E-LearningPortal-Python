# Generated by Django 3.1.1 on 2020-12-15 04:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_course_num_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(500)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
