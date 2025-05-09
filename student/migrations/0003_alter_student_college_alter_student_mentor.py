# Generated by Django 4.2.15 on 2025-03-22 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CollegeApp', '0002_alter_program_unique_together_and_more'),
        ('staff', '0003_alter_staff_college'),
        ('student', '0002_student_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='CollegeApp.college'),
        ),
        migrations.AlterField(
            model_name='student',
            name='mentor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student', to='staff.staff'),
        ),
    ]
