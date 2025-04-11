# Generated by Django 5.2 on 2025-04-10 12:27

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TableType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=50, unique=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='exam_app.course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('is_line', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
                ('course', models.ManyToManyField(blank=True, related_name='get_student', to='exam_app.course')),
                ('groups', models.ManyToManyField(blank=True, related_name='student', to='exam_app.group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='exam_app.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='exam_app.rooms')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='exam_app.tabletype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='group',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='exam_app.table'),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('descriptions', models.CharField(blank=True, max_length=500, null=True)),
                ('course', models.ManyToManyField(related_name='get_course', to='exam_app.course')),
                ('departments', models.ManyToManyField(related_name='get_department', to='exam_app.departments')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='group',
            name='teacher',
            field=models.ManyToManyField(related_name='get_teacher', to='exam_app.teacher'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message="Telefon raqam '+998XXXXXXXXX' formatida bo'lishi kerak!", regex='^\\+998\\d{9}$')])),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='exam_app_user_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='exam_app_user_permissions', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='user', to='exam_app.user'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='exam_app.user'),
        ),
    ]
