# Generated by Django 4.2.2 on 2023-10-30 15:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_tyre_country_alter_tyre_country_en_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='gallery',
            options={'verbose_name': 'Gallery', 'verbose_name_plural': 'Galleries'},
        ),
        migrations.AlterModelOptions(
            name='productstatistic',
            options={'verbose_name_plural': 'Product statistics'},
        ),
        migrations.AlterModelOptions(
            name='tyre',
            options={'verbose_name': 'Tyre', 'verbose_name_plural': 'Tyres'},
        ),
        migrations.AlterModelOptions(
            name='wheel',
            options={'verbose_name': 'Wheel', 'verbose_name_plural': 'Wheels'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_uk',
            field=models.CharField(max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=-1, scale=None, size=[300, 400], upload_to=shop.models.user_directory_path, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='productstatistic',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='productstatistic',
            name='sales_quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Sales quantity'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='brand',
            field=models.CharField(max_length=100, verbose_name='Brand'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='diameter',
            field=models.PositiveSmallIntegerField(verbose_name='Diameter'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='load_index',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Load index'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='price',
            field=models.IntegerField(verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='profile',
            field=models.DecimalField(decimal_places=1, max_digits=4, verbose_name='Profile'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='season',
            field=models.PositiveSmallIntegerField(choices=[(1, 'All season'), (2, 'Summer'), (3, 'Winter')], verbose_name='Season'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='sku',
            field=models.CharField(max_length=10, unique=True, verbose_name='sku'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='speed_index',
            field=models.CharField(blank=True, max_length=3, verbose_name='Speed index'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='spikes',
            field=models.BooleanField(default=False, verbose_name='Spikes'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'out stock'), (1, 'in stock'), (2, 'running out'), (3, 'coming soon')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='tyre',
            name='width',
            field=models.PositiveSmallIntegerField(verbose_name='Width'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='brand',
            field=models.CharField(max_length=100, verbose_name='Brand'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='color',
            field=models.CharField(blank=True, max_length=50, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='diameter',
            field=models.PositiveSmallIntegerField(verbose_name='Diameter'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='model',
            field=models.CharField(blank=True, max_length=100, verbose_name='Model'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='price',
            field=models.IntegerField(verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='sku',
            field=models.CharField(max_length=10, unique=True, verbose_name='sku'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'out stock'), (1, 'in stock'), (2, 'running out'), (3, 'coming soon')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Alloy'), (2, 'Steel')], verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='width',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Width'),
        ),
    ]
