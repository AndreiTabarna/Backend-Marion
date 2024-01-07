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
        # Check if the request is using HTTPS
        is_https = self.context['request'].is_secure()

        # Obține URL-ul de bază din contextul serializatorului
        base_url = self.context['request'].build_absolute_uri('/')[:-1]

        # Concatenează URL-ul imaginii
        image_url = f"{base_url}{obj.imagine.url}" if obj.imagine else None

        # If the request is using HTTPS, replace 'http://' with 'https://'
        if is_https and image_url:
            image_url = image_url.replace('http://', 'https://')

        return image_url

class ElementSerializer(serializers.ModelSerializer):
    # Adaugă un câmp pentru URL-ul de bază
    '''base_url = serializers.SerializerMethodField()'''

    class Meta:
        model = Element
        fields = '__all__'

    def get_base_url(self, obj):
        # Specifică URL-ul de bază
        return "http://127.0.0.1:8000"

    # Suprascrie metoda to_representation pentru a include URL-ul de bază în răspuns
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Verifică dacă cererea utilizează HTTPS
        is_https = self.context['request'].is_secure()

        # Obține URL-ul de bază din contextul serializatorului
        base_url = self.context['request'].build_absolute_uri('/')[:-1]

        # Concatenează URL-ul imaginii
        image_url = f"{base_url}{instance.imagine.url}" if instance.imagine else None

        # Dacă cererea utilizează HTTPS, înlocuiește 'http://' cu 'https://'
        if is_https and image_url:
            image_url = image_url.replace('http://', 'https://')

        representation['imagine'] = image_url
        return representation
