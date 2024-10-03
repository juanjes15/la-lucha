from django.forms import (
    Form,
    Textarea,
    CharField,
    DateInput,
    TextInput,
    ModelForm,
    HiddenInput,
    NumberInput,
    RadioSelect,
    IntegerField,
    SelectMultiple,
    ValidationError,
    ModelMultipleChoiceField,
)
from .models import Compra, Venta, Vacuna, Bovino, VacunaBovino


# NACIMIENTO
class BovinoForm(ModelForm):
    class Meta:
        model = Bovino
        exclude = [
            "compra",
            "venta",
            "vacunas",
            "precio_compra",
            "precio_venta",
            "peso_compra",
            "peso_venta",
        ]
        widgets = {
            "nombre": TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": DateInput(
                format=("%Y-%m-%d"), attrs={"type": "date", "class": "form-control"}
            ),
            "sexo": RadioSelect(),
            "madre": TextInput(attrs={"class": "form-control"}),
            "padre": TextInput(attrs={"class": "form-control"}),
            "topizado": RadioSelect(),
            "observaciones": Textarea(
                attrs={"class": "form-control", "style": "height: 100px"}
            ),
        }


# COMPRA
class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = "__all__"
        widgets = {
            "vendedor": TextInput(attrs={"class": "form-control"}),
            "fecha": DateInput(
                format=("%Y-%m-%d"), attrs={"type": "date", "class": "form-control"}
            ),
            "gastos": NumberInput(attrs={"class": "form-control"}),
            "observaciones": Textarea(
                attrs={"class": "form-control", "style": "height: 100px"}
            ),
        }


class CreateBovinosCompraForm(ModelForm):
    class Meta:
        model = Bovino
        exclude = [
            "compra",
            "venta",
            "vacunas",
            "precio_venta",
            "peso_venta",
        ]
        widgets = {
            "nombre": TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": DateInput(
                format=("%Y-%m-%d"), attrs={"type": "date", "class": "form-control"}
            ),
            "sexo": RadioSelect(),
            "madre": TextInput(attrs={"class": "form-control"}),
            "padre": TextInput(attrs={"class": "form-control"}),
            "precio_compra": NumberInput(attrs={"class": "form-control"}),
            "peso_compra": NumberInput(attrs={"class": "form-control"}),
            "topizado": RadioSelect(),
            "observaciones": Textarea(
                attrs={"class": "form-control", "style": "height: 100px"}
            ),
        }


# VENTA
class VentaForm(ModelForm):
    class Meta:
        model = Venta
        fields = "__all__"
        widgets = {
            "comprador": TextInput(attrs={"class": "form-control"}),
            "fecha": DateInput(
                format=("%Y-%m-%d"), attrs={"type": "date", "class": "form-control"}
            ),
            "gastos": NumberInput(attrs={"class": "form-control"}),
            "observaciones": Textarea(
                attrs={"class": "form-control", "style": "height: 100px"}
            ),
        }


class SelectBovinosVentaForm(Form):
    bovinos = ModelMultipleChoiceField(
        queryset=Bovino.objects.filter(venta__isnull=True),
        widget=SelectMultiple(attrs={"class": "form-select"}),
        label="Seleccionar bovinos para vender",
    )


class ModifyBovinosVentaForm(ModelForm):
    id = IntegerField(widget=HiddenInput())
    nombre = CharField(disabled=True)
    etapa_y_edad = CharField(disabled=True)

    class Meta:
        model = Bovino
        fields = ["id", "nombre", "etapa_y_edad", "precio_venta", "peso_venta"]
        widgets = {
            "precio_venta": NumberInput(attrs={"class": "form-control"}),
            "peso_venta": NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["nombre"].initial = self.instance.nombre
            self.fields["etapa_y_edad"].initial = self.instance.etapa_y_edad()


# VACUNA
class VacunaForm(ModelForm):
    class Meta:
        model = Vacuna
        fields = "__all__"
        widgets = {
            "vacunador": TextInput(attrs={"class": "form-control"}),
            "cc_vacunador": NumberInput(attrs={"class": "form-control"}),
            "tel_vacunador": NumberInput(attrs={"class": "form-control"}),
            "fecha": DateInput(
                format=("%Y-%m-%d"), attrs={"type": "date", "class": "form-control"}
            ),
            "precio": NumberInput(attrs={"class": "form-control"}),
            "observaciones": Textarea(
                attrs={"class": "form-control", "style": "height: 100px"}
            ),
        }


class SelectBovinosVacunaForm(Form):
    bovinos = ModelMultipleChoiceField(
        queryset=Bovino.objects.filter(venta__isnull=True),
        widget=SelectMultiple(attrs={"class": "form-select"}),
        label="Seleccionar bovinos para vacunar",
    )


class VacunaBovinoForm(ModelForm):
    bovino_id = IntegerField(widget=HiddenInput())
    nombre = CharField(disabled=True, required=False)
    etapa_y_edad = CharField(disabled=True, required=False)

    class Meta:
        model = VacunaBovino
        fields = ["bovino_id", "nombre", "etapa_y_edad", "tipo"]
        widgets = {
            "tipo": TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        bovino = kwargs.pop("bovino", None)
        super().__init__(*args, **kwargs)
        if bovino:
            self.fields["bovino_id"].initial = bovino.id
            self.fields["nombre"].initial = bovino.nombre
            self.fields["etapa_y_edad"].initial = bovino.etapa_y_edad()

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("tipo"):
            raise ValidationError("El tipo de vacuna es obligatorio.")
        return cleaned_data
