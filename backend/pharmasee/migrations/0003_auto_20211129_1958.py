# Generated by Django 3.0.14 on 2021-11-29 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pharmasee', '0002_auto_20211129_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='pill_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmasee.Pill'),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
