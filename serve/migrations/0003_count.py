# Generated by Django 2.0.2 on 2018-03-11 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serve', '0002_auto_20180311_2355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
