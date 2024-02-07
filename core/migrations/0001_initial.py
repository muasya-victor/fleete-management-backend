# Generated by Django 4.2.6 on 2024-01-15 18:25

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_code', models.CharField(blank=True, default='+254', max_length=4, null=True, validators=[django.core.validators.RegexValidator('^\\+\\d{1,3}$')])),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('avator', models.FileField(blank=True, null=True, upload_to='')),
                ('username', models.CharField(default='admin', max_length=128, unique=True)),
                ('password', models.CharField(default='123456', max_length=128)),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator('^\\d{9,10}$', 'Enter a valid phone number.')])),
                ('user_type', models.CharField(choices=[('vehicle_owner', 'Vehicle Owner'), ('mechanic', 'Mechanic')], default='mechanic', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(choices=[('Regular Maintenance', 'Regular Maintenance'), ('Diagnostic Services', 'Diagnostic Services'), ('Brake Services', 'Brake Services'), ('Tire Services', 'Tire Services'), ('Exhaust System Services', 'Exhaust System Services'), ('Transmission Services', 'Transmission Services'), ('Electrical System Services', 'Electrical System Services'), ('Cooling System Services', 'Cooling System Services'), ('Air Conditioning Services', 'Air Conditioning Services'), ('Fuel System Services', 'Fuel System Services'), ('Suspension and Steering Services', 'Suspension and Steering Services'), ('Engine Services', 'Engine Services'), ('Safety Inspections', 'Safety Inspections'), ('Preventive Maintenance', 'Preventive Maintenance')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UtilColumnsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehiclePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('comments', models.TextField(blank=True, null=True)),
                ('working_condition', models.BooleanField(default=True)),
                ('service_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.servicetype')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next_service_date', models.DateTimeField()),
                ('previous_service_date', models.DateTimeField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vehiclepart')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_number', models.CharField(max_length=255, unique=True)),
                ('general_condition', models.CharField(choices=[('healthy', 'Healthy'), ('unhealthy', 'Unhealthy')], default='healthy', max_length=20)),
                ('vehicle_type', models.CharField(max_length=40)),
                ('chassis_frame', models.CharField(max_length=255)),
                ('vehicle_model', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('body', models.CharField(max_length=255)),
                ('fuel', models.IntegerField()),
                ('engine_number', models.CharField(max_length=255, unique=True)),
                ('color', models.CharField(max_length=255)),
                ('reg_date', models.DateField()),
                ('gross_weight', models.IntegerField()),
                ('passengers', models.IntegerField()),
                ('tare_weight', models.CharField(max_length=255)),
                ('tax_class', models.CharField(max_length=255)),
                ('load_capacity', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle_parts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vehiclepart')),
            ],
        ),
    ]