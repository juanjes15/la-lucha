from django.contrib import admin
from .models import Compra, Venta, Vacuna, Bovino, VacunaBovino


admin.site.register(Compra)
admin.site.register(Venta)
admin.site.register(Vacuna)
admin.site.register(Bovino)
admin.site.register(VacunaBovino)
