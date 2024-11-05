from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import (
    CASCADE,
    Model,
    CharField,
    DateField,
    TextField,
    ForeignKey,
    BooleanField,
    ManyToManyField,
    SmallIntegerField,
    PositiveIntegerField,
    PositiveBigIntegerField,
)

# blank=False null=False -> default
# blank=True -> Campo puede quedar sin llenar en Front End
# null=True -> Asigna null al campo en la BD


class Compra(Model):
    vendedor = CharField(verbose_name="Nombre del vendedor", max_length=150)
    fecha = DateField(verbose_name="Fecha de la compra")
    gastos = PositiveIntegerField(verbose_name="Total gastos adicionales (Flete, pesada, etc)")
    observaciones = TextField(verbose_name="Observaciones (opcional)", blank=True)

    def __str__(self):
        return f"{self.vendedor} {self.fecha}"
    
    class Meta:
        ordering = ["fecha"]


class Venta(Model):
    comprador = CharField(verbose_name="Nombre del comprador", max_length=150)
    fecha = DateField(verbose_name="Fecha de la venta")
    gastos = PositiveIntegerField(verbose_name="Total gastos adicionales (Flete, pesada, etc)")
    observaciones = TextField(verbose_name="Observaciones (opcional)", blank=True)

    def __str__(self):
        return f"{self.comprador} {self.fecha}"
    
    class Meta:
        ordering = ["fecha"]


class Vacuna(Model):
    vacunador = CharField(verbose_name="Nombre del vacunador", max_length=150)
    cc_vacunador = PositiveBigIntegerField(verbose_name="Cédula del vacunador")
    tel_vacunador = PositiveBigIntegerField(verbose_name="Teléfono del vacunador")
    fecha = DateField(verbose_name="Fecha de la vacunación")
    precio = PositiveIntegerField(verbose_name="Pago total de la vacunación")
    observaciones = TextField(verbose_name="Observaciones (opcional)", blank=True)

    def __str__(self):
        return self.fecha
    
    class Meta:
        ordering = ["fecha"]


class Bovino(Model):
    nombre = CharField(verbose_name="Nombre", max_length=100)
    fecha_nacimiento = DateField(verbose_name="Fecha de nacimiento")
    sexo = BooleanField(verbose_name="Sexo", choices=((True, "Macho"), (False, "Hembra")))
    madre = CharField(verbose_name="Nombre de la madre (opcional)", blank=True, max_length=150)
    padre = CharField(verbose_name="Nombre del padre (opcional)", blank=True, max_length=150)
    precio_compra = PositiveIntegerField(verbose_name="Precio de compra", default=0)
    precio_venta = PositiveIntegerField(verbose_name="Precio de venta", default=0)
    peso_compra = SmallIntegerField(verbose_name="Peso al comprar (kg)", default=0)
    peso_venta = SmallIntegerField(verbose_name="Peso al vender (kg)", default=0)
    topizado = BooleanField(verbose_name="¿Está topizado?", default=False, choices=((True, "Si"), (False, "No")))
    capado = BooleanField(verbose_name="¿Está capado?", default=False, choices=((True, "Si"), (False, "No")))
    observaciones = TextField(verbose_name="Observaciones (opcional)", blank=True)
    compra = ForeignKey(Compra, on_delete=CASCADE, blank=True, null=True)
    venta = ForeignKey(Venta, on_delete=CASCADE, blank=True, null=True)
    vacunas = ManyToManyField(Vacuna, through="VacunaBovino", blank=True)

    def __str__(self):
        return self.nombre

    def calcular_edad(self):
        hoy = timezone.now().date()
        diff = relativedelta(hoy, self.fecha_nacimiento)
        return diff.years, diff.months

    def etapa_de_vida(self):
        años, meses = self.calcular_edad()
        edad_meses = años * 12 + meses

        if self.sexo:
            if edad_meses <= 6:
                return "Becerro"
            elif 6 < edad_meses <= 12:
                return "Ternero"
            elif (12 < edad_meses <= 36) or self.capado:
                return "Novillo"
            else:
                return "Toro"
        else:
            if edad_meses <= 6:
                return "Becerra"
            elif 6 < edad_meses <= 12:
                return "Ternera"
            elif 12 < edad_meses <= 36:
                return "Novilla"
            else:
                return "Vaca"

    def etapa_y_edad(self):
        años, meses = self.calcular_edad()
        etapa = self.etapa_de_vida()

        if años == 0:
            return f"{etapa} ({meses} meses)"
        elif años == 1:
            if meses == 0:
                return f"{etapa} (1 año)"
            else:
                return f"{etapa} (1 año, {meses} meses)"
        else:
            if meses == 0:
                return f"{etapa} ({años} años)"
            else:
                return f"{etapa} ({años} años, {meses} meses)"
            
    class Meta:
        ordering = ["fecha_nacimiento"]


class VacunaBovino(Model):
    vacuna = ForeignKey(Vacuna, on_delete=CASCADE)
    bovino = ForeignKey(Bovino, on_delete=CASCADE)
    tipo = CharField(verbose_name="Tipo de vacuna", max_length=25)

    def __str__(self):
        return "{}_{}".format(self.bovino.__str__(), self.vacuna.__str__())
