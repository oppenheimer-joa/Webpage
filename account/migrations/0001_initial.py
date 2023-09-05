# Generated by Django 4.0.3 on 2023-09-04 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('user_pw', models.CharField(blank=True, max_length=100, null=True)),
                ('user_nm', models.CharField(blank=True, max_length=20, null=True)),
                ('user_email', models.CharField(blank=True, max_length=100, null=True)),
                ('user_register_dt', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_info',
                'managed': False,
            },
        ),
    ]
