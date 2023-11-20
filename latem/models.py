from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    telephone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    isAdmin=models.BooleanField(default=False)
    class Meta :
        ordering = ['id']

class Items(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    class Meta :
        ordering = ['id']

class DescriptionItems(models.Model):
    DESCRIPTION_CHOICES = [
    ('charac','charac'),
    ('finitions','finitions')
    ]
    parent_item=models.ForeignKey(Items, on_delete=models.CASCADE, related_name='child_desc_items')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    parent_description=models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_desc', blank=True, null=True)
    description_type = models.CharField(max_length=30, choices=DESCRIPTION_CHOICES, default='charac')
    apply_on_all_items=models.BooleanField(default=False)
    level=models.IntegerField()
    class Meta :
        ordering = ['id']

class Devis(models.Model):
    STATUS_CHOICES = [
        ('réceptionné', 'Réceptionné'),
        ('devis envoyé', 'Devis envoyé'),
        ('validé par le client', 'Validé par le client'),
        ('payé', 'Payé'),
        ('réalisé', 'Réalisé'),
        ('clôturé', 'Clôturé')
    ]
    clientId = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='devis_client')
    created_at = models.DateTimeField(auto_now_add=True)
    status =models.CharField(max_length=100, choices=STATUS_CHOICES, default='réceptionné')
    responsableId = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='devis_responsable', blank=True, null=True)
    total = models.IntegerField(null=True, blank=True, default=0)
    class Meta :
        ordering = ['id']  

class DevisFile(models.Model):
    devisId= models.ForeignKey(Devis, on_delete=models.CASCADE, related_name='devis_file')
    file = models.FileField(upload_to='devis_files/')
    class Meta :
        ordering = ['id']

class LignesItemsDevis(models.Model):
    devisId = models.ForeignKey(Devis, on_delete=models.CASCADE, related_name='lignes_devis')
    itemId = models.ForeignKey(Items, on_delete=models.SET_DEFAULT, related_name='lignes_items', default=None, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    textCustom = models.TextField(null=True, blank=True, default=None)
    class Meta :
        ordering = ['id']

class LignesDescDevis(models.Model):
    LignesItemsDevisId = models.ForeignKey(LignesItemsDevis, on_delete=models.CASCADE, related_name='lignes_desc_devis')
    descriptionItems = models.ForeignKey(DescriptionItems, on_delete=models.CASCADE, related_name='lignes_desc_items', null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    textCustom = models.TextField(null=True, blank=True, default=None)
    class Meta :
        ordering = ['id']
