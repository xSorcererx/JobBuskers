# Generated by Django 4.0.5 on 2023-04-28 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_usertokens'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertokens',
            name='preference',
            field=models.CharField(choices=[('Architechture/ Interior Designing', 'Architechture/ Interior Designing'), ('IT & Telecommunication', 'IT & Telecommunication'), ('Teaching/ Education', 'Teaching/ Education'), ('NGO/ INGO', 'NGO/ INGO'), ('Graphics/ Designing', 'Graphics/ Designing'), ('Hospitality', 'Hospitality'), ('Sales/ Public Relation', 'Sales/ Public Relation'), ('Legal Services', 'Legal Services'), ('Other', 'Other')], default='Other', max_length=200, verbose_name='Preference'),
        ),
    ]