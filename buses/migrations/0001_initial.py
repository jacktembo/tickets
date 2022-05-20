# Generated by Django 4.0.4 on 2022-05-20 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('bus_full_name', models.CharField(max_length=50)),
                ('bus_short_name', models.CharField(editable=False, max_length=20, primary_key=True, serialize=False)),
                ('number_of_seats', models.IntegerField()),
                ('mobile_money_number', models.CharField(help_text='Enter the 10 digit Mobile Money number for receiving money.', max_length=10)),
                ('bus_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Buses',
            },
        ),
        migrations.CreateModel(
            name='BusCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
                ('company_phone_number', models.CharField(max_length=50)),
                ('company_email', models.EmailField(max_length=64)),
                ('address', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Login Username')),
            ],
            options={
                'verbose_name_plural': 'Bus Companies',
            },
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_place', models.CharField(max_length=50)),
                ('destination', models.CharField(max_length=50)),
                ('time', models.TimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route', to='buses.bus')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_number', models.CharField(editable=False, max_length=20, primary_key=True, serialize=False, unique=True)),
                ('date_bought', models.DateField(auto_now_add=True)),
                ('passenger_phone', models.CharField(max_length=12)),
                ('passenger_first_name', models.CharField(max_length=50)),
                ('passenger_last_name', models.CharField(max_length=50)),
                ('departure_date', models.DateField()),
                ('seat_number', models.IntegerField()),
                ('sold_offline', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('scanned', models.BooleanField(default=False, help_text='Designates whether a Ticket has already been scanned')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buses.bus')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buses.route')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('is_available', models.BooleanField()),
                ('verbose_name', models.CharField(blank=True, max_length=50, null=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buses.bus')),
            ],
        ),
        migrations.CreateModel(
            name='BusImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tickets/buses', verbose_name='Upload Bus Image')),
                ('bus', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='buses.bus')),
            ],
        ),
        migrations.CreateModel(
            name='BusCompanyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tickets/buscompanies', verbose_name='Upload Company Logo')),
                ('bus_company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='buses.buscompany')),
            ],
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buses', to='buses.buscompany'),
        ),
    ]
