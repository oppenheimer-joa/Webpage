# Generated by Django 4.2.5 on 2023-09-14 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20230911_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postname', models.CharField(max_length=50)),
                ('contents', models.TextField()),
            ],
        ),
    ]
