from django.contrib import admin
from .models import Element

class ElementAdmin(admin.ModelAdmin):
    list_display = ('get_element_name',)

    def get_element_name(self, obj):
        # Extrage numele dintre primul și al doilea caracter "/"
        if '/' in obj.url:
            start_index = obj.url.index('/') + 1
            end_index = obj.url.index('/', start_index)
            return obj.url[start_index:end_index]
        return obj.url  # Dacă nu există "/" sau obiectul nu are un nume între "/", afișează întregul URL

    get_element_name.short_description = 'Nume Element'

admin.site.register(Element, ElementAdmin)

