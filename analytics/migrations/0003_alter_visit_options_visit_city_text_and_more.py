# Generated by Django 4.2.16 on 2025-01-28 18:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_event'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visit',
            options={'verbose_name': 'Visit', 'verbose_name_plural': 'Visits'},
        ),
        migrations.AddField(
            model_name='visit',
            name='city_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='country_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='ip_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='left_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='mobile',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='visit',
            name='uid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
    ]
