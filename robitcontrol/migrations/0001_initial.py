# Generated by Django 3.2.4 on 2021-06-05 11:45

from django.db import migrations, models
import django.db.models.deletion
import robitcontrol.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('webhooksocket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('key', models.CharField(db_index=True, default=robitcontrol.models.random_ident, max_length=64, unique=True)),
                ('update_bridge', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='webhooksocket.bridge')),
            ],
        ),
    ]
