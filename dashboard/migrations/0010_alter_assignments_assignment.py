# Generated by Django 3.2.4 on 2021-07-02 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_categories_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='assignment',
            field=models.FileField(default='uploads/profile_background/default.jpg', upload_to='uploads/student_assignments'),
        ),
    ]
