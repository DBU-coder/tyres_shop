# Generated by Django 4.2.2 on 2023-08-01 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_tyre_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wheel',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='dia',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='et',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='pcd',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
