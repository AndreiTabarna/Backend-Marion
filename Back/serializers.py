# serializers.py

from rest_framework import serializers
from .models import Element

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    # Adaugă câmpuri pentru URL-ul complet al imaginii, id-ul elementului și URL-ul din baza de date
    image_url = serializers.SerializerMethodField()
    element_id = serializers.IntegerField(source='id', read_only=True)
    element_url = serializers.CharField(source='url', read_only=True)

    class Meta:
        model = Element
        fields = ['image_url', 'element_id', 'element_url']


    def get_image_url(self, obj):
        # Obține URL-ul de bază din contextul serializatorului
        base_url = self.context['request'].build_absolute_uri('/')[:-1]

        # Construiește URL-ul imaginii și adaugă "s" la sfârșitul "http", dacă este cazul
        image_url = f"{base_url}{obj.imagine.url}" if obj.imagine else None
        if image_url and image_url.startswith('http://'):
            image_url = image_url.replace('http://', 'https://')

        return image_url

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Obține URL-ul de bază din contextul serializatorului
        base_url = self.context['request'].build_absolute_uri('/')[:-1]

        # Actualizează URL-ul imaginii, adăugând "s" la sfârșitul "http", dacă este cazul
        image_url = f"{base_url}{instance.imagine.url}" if instance.imagine else None
        if image_url and image_url.startswith('http://'):
            image_url = image_url.replace('http://', 'https://')

        representation['imagine'] = image_url

        return representation

