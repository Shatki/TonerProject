# Generated by Django 2.0.1 on 2018-02-16 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0001_initial'),
        ('contractor', '0001_initial'),
        ('business', '0005_auto_20170520_0226'),
        ('document', '0005_auto_20180212_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, verbose_name='номер документа')),
                ('date', models.DateField(verbose_name='дата документа')),
                ('delete', models.BooleanField(default=True, verbose_name='Черновик/Подлежит удалению')),
                ('enable', models.BooleanField(default=False, verbose_name='действующий документ')),
                ('created', models.DateTimeField(verbose_name='время/дата создания документа')),
                ('modified', models.DateTimeField(verbose_name='время/дата изменения документа')),
                ('contract', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_contract', to='document.Contract', verbose_name='контракт')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_creator', to=settings.AUTH_USER_MODEL, verbose_name='автор документа')),
                ('emitter', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_emitter', to='contractor.Contractor', verbose_name='организация эмитент')),
            ],
            options={
                'verbose_name': 'документ',
                'verbose_name_plural': 'документы',
                'db_table': 'document',
            },
        ),
        migrations.CreateModel(
            name='DocumentTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='номер в документк')),
                ('quantity', models.FloatField(default=0.0, verbose_name='количество')),
                ('cost', models.FloatField(default=0.0, null=True, verbose_name='стоимость единицы продукта без налогов')),
                ('country', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.Country', verbose_name='страна происхождения')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.Document', verbose_name='накладная')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Product', verbose_name='продукт')),
                ('measure', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='system.Measure', verbose_name='единица измерения')),
                ('tax', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.Tax', verbose_name='налоговая ставка')),
            ],
            options={
                'verbose_name': 'продукт в документе',
                'verbose_name_plural': 'продукция в документе',
                'db_table': 'document_items',
            },
        ),
        migrations.RemoveField(
            model_name='consignment',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='consignment',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='consignment',
            name='emitter',
        ),
        migrations.RemoveField(
            model_name='consignment',
            name='items',
        ),
        migrations.RemoveField(
            model_name='consignment',
            name='modificator',
        ),
        migrations.RemoveField(
            model_name='consignment',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='consignment',
            name='type',
        ),
        migrations.RemoveField(
            model_name='consignmenttable',
            name='consignment',
        ),
        migrations.RemoveField(
            model_name='consignmenttable',
            name='country',
        ),
        migrations.RemoveField(
            model_name='consignmenttable',
            name='item',
        ),
        migrations.RemoveField(
            model_name='consignmenttable',
            name='measure',
        ),
        migrations.RemoveField(
            model_name='consignmenttable',
            name='tax',
        ),
        migrations.AddField(
            model_name='doctype',
            name='action',
            field=models.CharField(default=1, max_length=30, verbose_name='Название документа (например, Реализация)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='doctype',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Название документа (например, Накладная)'),
        ),
        migrations.AlterField(
            model_name='doctype',
            name='type',
            field=models.CharField(max_length=30, verbose_name='Тип документа (например, Consignment)'),
        ),
        migrations.AlterModelTable(
            name='doctype',
            table='doctype',
        ),
        migrations.DeleteModel(
            name='Consignment',
        ),
        migrations.DeleteModel(
            name='ConsignmentTable',
        ),
        migrations.AddField(
            model_name='document',
            name='items',
            field=models.ManyToManyField(related_name='document_items', through='document.DocumentTable', to='system.Product', verbose_name='продукция в документе'),
        ),
        migrations.AddField(
            model_name='document',
            name='modificator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_modificator', to=settings.AUTH_USER_MODEL, verbose_name='изменил документ'),
        ),
        migrations.AddField(
            model_name='document',
            name='receiver',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_receiver', to='contractor.Contractor', verbose_name='организация контрагент'),
        ),
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_items', to='document.DocType', verbose_name='продукция'),
        ),
    ]
