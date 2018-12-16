# Generated by Django 2.1.3 on 2018-11-26 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info_extractor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=8)),
                ('market', models.CharField(max_length=5)),
            ],
        ),
        migrations.RemoveField(
            model_name='reportanalysis',
            name='instrument',
        ),
        migrations.RemoveField(
            model_name='reportanalysis',
            name='market',
        ),
        migrations.AddField(
            model_name='reportanalysis',
            name='instrumentid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='info_extractor.Instrument'),
            preserve_default=False,
        ),
    ]
