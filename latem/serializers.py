from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

class DescriptionItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionItems
        fields = '__all__'

class DevisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devis
        fields = '__all__'

class DevisFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevisFile
        fields = '__all__'

class LignesItemsDevisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LignesItemsDevis
        fields = '__all__'

class LignesDescDevisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LignesDescDevis
        fields = '__all__'


