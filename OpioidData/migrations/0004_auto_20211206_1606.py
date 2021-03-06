# Generated by Django 3.2.9 on 2021-12-06 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OpioidData', '0003_credential_prescribercredential_specialtie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty_type', models.CharField(max_length=70, unique=True)),
            ],
            options={
                'db_table': 'specialty',
            },
        ),
        migrations.CreateModel(
            name='Triple',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
            ],
            options={
                'db_table': 'pd_triple',
            },
        ),
        migrations.DeleteModel(
            name='Specialtie',
        ),
        migrations.RemoveField(
            model_name='prescribercredential',
            name='credential_code',
        ),
        migrations.AddField(
            model_name='credential',
            name='credential_code',
            field=models.IntegerField(default=10000000000, unique=True),
        ),
        migrations.AddField(
            model_name='prescriber',
            name='isopioid_prescriber',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='prescriber',
            name='specialty',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='prescribercredential',
            name='credential',
            field=models.ForeignKey(default=110, on_delete=django.db.models.deletion.DO_NOTHING, to='OpioidData.credential', to_field='credential_code'),
        ),
        migrations.AlterField(
            model_name='drug',
            name='drugname',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='prescriber',
            name='Gender',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.AlterField(
            model_name='prescriber',
            name='State',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='prescriber',
            name='npi',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='prescribercredential',
            name='npi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='OpioidData.prescriber', to_field='npi'),
        ),
        migrations.AddField(
            model_name='triple',
            name='drugname',
            field=models.ForeignKey(db_column='drugname', on_delete=django.db.models.deletion.DO_NOTHING, to='OpioidData.drug', to_field='drugname'),
        ),
        migrations.AddField(
            model_name='triple',
            name='prescriberid',
            field=models.ForeignKey(db_column='prescriberid', on_delete=django.db.models.deletion.DO_NOTHING, to='OpioidData.prescriber', to_field='npi'),
        ),
    ]
