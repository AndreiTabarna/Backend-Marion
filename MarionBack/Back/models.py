# models.py

from django.db import models

class Element(models.Model):
    imagine = models.ImageField(upload_to='imagini/')
    perioada = models.TextField()
    tarif = models.TextField()
    telefon = models.TextField()
    url = models.CharField(max_length=255)
    tara = models.CharField(max_length=255, default='Nedefinit')
    oras = models.CharField(max_length=255, default='Nedefinit')
    transport = models.CharField(max_length=255, default='Nedefinit')
    program = models.TextField()
    include = models.TextField()
    nu_include = models.TextField()
    acte = models.TextField()
    important = models.TextField()

