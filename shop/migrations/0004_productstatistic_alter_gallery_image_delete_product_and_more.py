# Generated by Django 4.2.2 on 2023-08-17 17:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('shop', '0003_alter_gallery_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('sales_quantity', models.PositiveIntegerField(default=0)),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ('tyre', 'wheel')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=-1, scale=None, size=[300, 400], upload_to=shop.models.user_directory_path),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.AddIndex(
            model_name='productstatistic',
            index=models.Index(fields=['content_type', 'object_id'], name='shop_produc_content_c49b40_idx'),
        ),
    ]
