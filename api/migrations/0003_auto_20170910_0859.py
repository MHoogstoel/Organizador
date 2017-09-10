# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-10 08:59
from __future__ import unicode_literals

from django.db import migrations, models


def move_existing_contacts(apps, _):
    Personne = apps.get_model("api", "Personne")
    for p in Personne.objects.all():
        contacts = p.contacts.all()
        if len(contacts) > 0:
            p.contact_nom = contacts[0].nom + ' ' + contacts[0].prenom
            p.contact_principal_tel = contacts[0].telephone
            p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170909_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='personne',
            name='contact_nom',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='personne',
            name='contact_principal_tel',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='personne',
            name='contact_secondaire_tel',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.RunPython(move_existing_contacts),
        migrations.RemoveField(
            model_name='personne',
            name='contacts',
        ),
    ]