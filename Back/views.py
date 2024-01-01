from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Element
from .serializers import ElementSerializer
from .serializers import ImageSerializer
from urllib.parse import unquote

class ElementListCreateView(generics.ListCreateAPIView):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer

class ImageListView(APIView):
    def get(self, request):
        # Obține parametrii de filtrare din query string
        oras_param = request.query_params.get('Oras', None)
        tara_param = request.query_params.get('Tara', None)
        transport_param = request.query_params.get('Transport', None)

        # Filtrare în funcție de parametrii
        queryset = Element.objects.all()
        if oras_param:
            # Folosește __icontains pentru a căuta în întregul șir, nu doar la început
            queryset = queryset.filter(oras__icontains=oras_param)
        if tara_param:
            queryset = queryset.filter(tara__icontains=tara_param)
        if transport_param:
            queryset = queryset.filter(transport=transport_param)

        # Aici setezi contextul pentru serializer
        serializer = ImageSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
        
class ElementDetailView(APIView):
    def get(self, request, element_id):
        try:
            element = Element.objects.get(id=element_id)
        except Element.DoesNotExist:
            return Response({"error": "Element not found"}, status=404)

        serializer = ElementSerializer(element, context={'request': request})
        return Response(serializer.data)
        
class ElementDetailViewByURL(APIView):
    def get(self, request):
        # Obține URL-ul din query string
        url_param = request.query_params.get('url', None)

        if not url_param:
            return Response({"error": "URL parameter is required"}, status=400)

        # Decodifică URL-ul și înlătură eventualele spații în plus
        decoded_url = unquote(url_param).strip()

        try:
            # Înlătură query string-ul din URL pentru a găsi elementul
            element = Element.objects.get(url__startswith=decoded_url.split('?')[0])
        except Element.DoesNotExist:
            return Response({"error": "Element not found"}, status=404)

        serializer = ElementSerializer(element, context={'request': request})
        return Response(serializer.data)
        
class UniqueValuesView(APIView):
    def get(self, request):
        # Obține toate valorile unice pentru 'tara', 'oras' și 'transport'
        unique_tari = sorted(self.get_unique_tari())
        unique_orase = sorted(self.get_unique_orase())
        unique_transport = sorted(Element.objects.values_list('transport', flat=True).distinct())

        response_data = {
            'unique_tari': unique_tari,
            'unique_orase': unique_orase,
            'unique_transport': unique_transport,
        }

        return Response(response_data)

    def get_unique_tari(self):
        # Obține toate valorile pentru 'tara'
        all_tari = Element.objects.values_list('tara', flat=True)
        
        # Concatenează toate valorile și împarte-le după virgulă
        all_tari = ','.join(all_tari).split(',')
        
        # Elimină spațiile albe și obține valorile unice, apoi sortează alfabetic
        unique_tari = sorted(set(map(str.strip, all_tari)))

        return unique_tari

    def get_unique_orase(self):
        # Obține toate valorile pentru 'oras'
        all_orase = Element.objects.values_list('oras', flat=True)
        
        # Concatenează toate valorile și împarte-le după virgulă
        all_orase = ','.join(all_orase).split(',')
        
        # Elimină spațiile albe și obține valorile unice, apoi sortează alfabetic
        unique_orase = sorted(set(map(str.strip, all_orase)))

        return unique_orase
        
class SimilarElementsView(APIView):
    def get(self, request, element_id):
        try:
            current_element = Element.objects.get(id=element_id)
        except Element.DoesNotExist:
            return Response({"error": "Element not found"}, status=404)

        # Obține tariful pentru elementul curent (eliminând textul și păstrând doar numerele)
        current_tarif = self.extract_tarif(current_element.tarif)

        # Obține cele mai apropiate 4 elemente după tarif, excludând elementul curent
        similar_elements = self.get_similar_elements(current_tarif, current_element)

        # Serializare și răspuns API
        serializer = ImageSerializer(similar_elements, many=True, context={'request': request})
        return Response(serializer.data)

    def extract_tarif(self, tarif_text):
        # Elimină textul și păstrează doar numerele
        tarif_number = int(''.join(filter(str.isdigit, tarif_text)))

        # Verifică dacă "lei" apare în text și împarte numărul la 5 în acest caz
        if "lei" in tarif_text:
            tarif_number /= 5

        return tarif_number

    def get_similar_elements(self, current_tarif, current_element):
        # Obține toate elementele și sortează-le după diferența de tarif față de elementul curent
        all_elements = Element.objects.exclude(id=current_element.id)  # Exclude elementul curent
        sorted_elements = sorted(all_elements, key=lambda x: abs(current_tarif - self.extract_tarif(x.tarif)))

        # Alege primele 4 elemente
        similar_elements = sorted_elements[:3]

        return similar_elements

