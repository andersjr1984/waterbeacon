# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-06-04 02:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EpaWaterSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PWSName', models.CharField(max_length=255)),
                ('PWSId', models.CharField(max_length=255, unique=True)),
                ('CitiesServed', models.CharField(max_length=4000, null=True)),
                ('StateCode', models.CharField(db_index=True, max_length=10, null=True)),
                ('ZipCodesServed', models.CharField(db_index=True, max_length=4000, null=True)),
                ('CountiesServed', models.CharField(max_length=4000, null=True)),
                ('EPARegion', models.CharField(max_length=10, null=True)),
                ('PWSTypeCode', models.CharField(max_length=50)),
                ('PrimarySourceCode', models.CharField(max_length=50, null=True)),
                ('PrimarySourceDesc', models.CharField(max_length=255, null=True)),
                ('PopulationServedCount', models.IntegerField(null=True)),
                ('PWSActivityCode', models.CharField(max_length=10, null=True)),
                ('PWSActivityDesc', models.CharField(max_length=255, null=True)),
                ('OwnerTypeCode', models.CharField(max_length=10, null=True)),
                ('OwnerDesc', models.CharField(max_length=255, null=True)),
                ('QtrsWithVio', models.IntegerField(null=True)),
                ('QtrsWithSNC', models.IntegerField(null=True)),
                ('SeriousViolator', models.CharField(max_length=10, null=True)),
                ('HealthFlag', models.CharField(max_length=10, null=True)),
                ('MrFlag', models.CharField(max_length=10, null=True)),
                ('PnFlag', models.CharField(max_length=10, null=True)),
                ('OtherFlag', models.CharField(max_length=10, null=True)),
                ('NewVioFlag', models.CharField(max_length=10, null=True)),
                ('RulesVio3yr', models.IntegerField(null=True)),
                ('RulesVio', models.IntegerField(null=True)),
                ('Viopaccr', models.IntegerField(db_index=True, null=True)),
                ('Vioremain', models.IntegerField(db_index=True, null=True)),
                ('Viofeanot', models.IntegerField(null=True)),
                ('Viortcfea', models.IntegerField(null=True)),
                ('Viortcnofea', models.IntegerField(null=True)),
                ('Ifea', models.CharField(max_length=255, null=True)),
                ('Feas', models.CharField(max_length=255, null=True)),
                ('SDWDateLastIea', models.DateField(null=True)),
                ('SDWDateLastIeaEPA', models.DateField(null=True)),
                ('SDWDateLastIeaSt', models.DateField(null=True)),
                ('SDWDateLastFea', models.DateField(null=True)),
                ('SDWDateLastFeaEPA', models.DateField(null=True)),
                ('SDWDateLastFeaSt', models.DateField(null=True)),
                ('SDWAContaminantsInViol3yr', models.CharField(max_length=4000, null=True)),
                ('SDWAContaminantsInCurViol', models.CharField(max_length=4000, null=True)),
                ('PbAle', models.CharField(max_length=50, null=True)),
                ('CuAle', models.CharField(max_length=50, null=True)),
                ('Rc350Viol', models.IntegerField(null=True)),
                ('DfrUrl', models.CharField(max_length=1000, null=True)),
                ('FIPSCodes', models.CharField(max_length=1000, null=True)),
                ('SNC', models.CharField(max_length=255, null=True)),
                ('GwSwCode', models.CharField(max_length=10, null=True)),
                ('SDWA3yrComplQtrsHistory', models.CharField(max_length=4000, null=True)),
                ('SDWAContaminants', models.CharField(max_length=4000, null=True)),
                ('PbViol', models.IntegerField(null=True)),
                ('CuViol', models.IntegerField(null=True)),
                ('LeadAndCopperViol', models.IntegerField(null=True)),
                ('TribalFlag', models.NullBooleanField()),
                ('FeaFlag', models.NullBooleanField()),
                ('IeaFlag', models.NullBooleanField()),
                ('SNCFlag', models.NullBooleanField()),
                ('CurrVioFlag', models.IntegerField(null=True)),
                ('VioFlag', models.IntegerField(null=True)),
                ('Insp5yrFlag', models.NullBooleanField()),
                ('Sansurvey5yr', models.IntegerField(null=True)),
                ('SignificantDeficiencyCount', models.IntegerField(null=True)),
                ('SDWDateLastVisit', models.DateField(null=True)),
                ('SDWDateLastVisitEPA', models.DateField(null=True)),
                ('SDWDateLastVisitState', models.DateField(null=True)),
                ('SDWDateLastVisitLocal', models.DateField(null=True)),
                ('SiteVisits5yrAll', models.IntegerField(null=True)),
                ('SiteVisits5yrInspections', models.IntegerField(null=True)),
                ('SiteVisits5yrOther', models.IntegerField(null=True)),
                ('MaxScore', models.IntegerField(null=True)),
            ],
        ),
    ]
