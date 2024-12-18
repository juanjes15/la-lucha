from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import (
    VentaForm,
    BovinoForm,
    CompraForm,
    VacunaForm,
    VacunaBovinoForm,
    SelectBovinosForm,
    ModifyBovinosVentaForm,
    CreateBovinosCompraForm,
)
from .models import Compra, Bovino, Venta, Vacuna, VacunaBovino
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms import modelformset_factory, formset_factory
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Sum


# HOME GANADERIA
@login_required
def home_g(request):
    # Búsqueda y paginación
    search = request.GET.get("q")
    page_num = request.GET.get("page", 1)
    bovinos = Bovino.objects.filter(venta__isnull=True)
    if search:
        bovinos = bovinos.filter(
            Q(nombre__icontains=search)
            | Q(fecha_nacimiento__icontains=search)
            | Q(madre__icontains=search)
        )
    page = Paginator(object_list=bovinos, per_page=9).get_page(page_num)

    # Entrada de datos
    inputs = [
        {
            "name": "Registrar bovino",
            "url": reverse("create_bovino"),
            "img": "https://i.imgur.com/gIhLm9z.jpeg",
        },
        {
            "name": "Registrar compra",
            "url": reverse("create_compra"),
            "img": "https://i.imgur.com/CpmmhsG.jpeg",
        },
        {
            "name": "Registrar venta",
            "url": reverse("create_venta"),
            "img": "https://i.imgur.com/kTgh73e.jpeg",
        },
        {
            "name": "Registrar vacuna",
            "url": reverse("create_vacuna"),
            "img": "https://i.imgur.com/S1XnKpq.jpeg",
        },
    ]

    # Historiales
    logs = [
        {
            "name": "Bovinos vendidos",
            "url": reverse("all_bovinos"),
            "img": "https://i.imgur.com/sJYrFgc.jpeg",
        },
        {
            "name": "Compras",
            "url": reverse("all_compras"),
            "img": "https://i.imgur.com/CpmmhsG.jpeg",
        },
        {
            "name": "Ventas",
            "url": reverse("all_ventas"),
            "img": "https://i.imgur.com/kTgh73e.jpeg",
        },
        {
            "name": "Vacunas",
            "url": reverse("all_vacunas"),
            "img": "https://i.imgur.com/S1XnKpq.jpeg",
        },
    ]

    # Datos enviados al template
    context = {"page": page, "inputs": inputs, "logs": logs}

    return render(request=request, template_name="home_g.html", context=context)


# BOVINO
@login_required
def create_bovino(request):
    # Vista para crear un bovino (por nacimiento)
    if request.method == "POST":
        form = BovinoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home_g")
    else:
        form = BovinoForm()
    return render(request, "create_bovino.html", {"form": form})


@login_required
def detail_bovino(request, bovino_id):
    # Vista para ver el detalle de un bovino
    bovino = get_object_or_404(Bovino, id=bovino_id)
    return render(request, "detail_bovino.html", {"bovino": bovino})


@login_required
def edit_bovino(request, bovino_id):
    # Vista para editar un bovino
    bovino = get_object_or_404(Bovino, id=bovino_id)
    is_born = bovino.compra is None
    if request.method == "POST":
        form = CreateBovinosCompraForm(request.POST, instance=bovino)
        if form.is_valid():
            bovino.save()
            return redirect("detail_bovino", bovino_id=bovino_id)
    else:
        form = CreateBovinosCompraForm(instance=bovino)
    return render(
        request,
        "edit_bovino.html",
        {"form": form, "bovino_id": bovino_id, "is_born": is_born},
    )


@login_required
def all_bovinos(request):
    # Página para mostrar los bovinos vendidos
    search = request.GET.get("q")
    page_num = request.GET.get("page", 1)
    bovinos = Bovino.objects.filter(venta__isnull=False)
    if search:
        bovinos = bovinos.filter(
            Q(nombre__icontains=search)
            | Q(fecha_nacimiento__icontains=search)
            | Q(madre__icontains=search)
        )
    page = Paginator(object_list=bovinos, per_page=9).get_page(page_num)

    context = {"page": page}

    return render(request=request, template_name="all_bovinos.html", context=context)


# COMPRA
@login_required
def create_compra(request):
    # Vista para crear una compra
    if request.method == "POST":
        form = CompraForm(data=request.POST)
        if form.is_valid():
            compra = form.save()
            return redirect("create_bovinos_compra", compra_id=compra.id)
    else:
        form = CompraForm()
    return render(request, "compra/create.html", {"form": form})


@login_required
def edit_compra(request, compra_id):
    # Vista para editar una compra
    compra = get_object_or_404(Compra, id=compra_id)
    if request.method == "POST":
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            compra.save()
            return redirect("summary_compra", compra_id=compra_id)
    else:
        form = CompraForm(instance=compra)
    return render(
        request,
        "compra/edit.html",
        {"form": form, "compra_id": compra_id},
    )


@login_required
def create_bovinos_compra(request, compra_id):
    # Vista para crear bovinos (por medio de una compra)
    compra = get_object_or_404(Compra, id=compra_id)

    if request.method == "POST":
        num_bovinos = int(request.POST.get("num_bovinos", 1))
        forms = [
            CreateBovinosCompraForm(request.POST, prefix=str(x))
            for x in range(num_bovinos)
        ]
        if all([form.is_valid() for form in forms]):
            for form in forms:
                bovino = form.save(commit=False)
                bovino.compra = compra
                bovino.save()
            return redirect("summary_compra", compra_id=compra.id)
    else:
        num_bovinos = int(request.GET.get("num_bovinos", 1))
        forms = [CreateBovinosCompraForm(prefix=str(x)) for x in range(num_bovinos)]

    return render(
        request,
        "compra/create_bovinos.html",
        {"forms": forms, "compra": compra, "num_bovinos": num_bovinos},
    )


@login_required
def summary_compra(request, compra_id):
    # Vista para ver el resumen de la compra
    compra = get_object_or_404(Compra, id=compra_id)
    bovinos_comprados = Bovino.objects.filter(compra=compra)
    precio_bovinos = (
        bovinos_comprados.aggregate(Sum("precio_compra"))["precio_compra__sum"] or 0
    )
    total_compra = precio_bovinos + compra.gastos
    return render(
        request,
        "compra/summary.html",
        {
            "compra": compra,
            "bovinos": bovinos_comprados,
            "precio_bovinos": precio_bovinos,
            "total_compra": total_compra,
        },
    )


@login_required
def all_compras(request):
    # Página para mostrar todas las compras
    search = request.GET.get("q")
    page_num = request.GET.get("page", 1)
    compras = Compra.objects.all()
    if search:
        compras = compras.filter(
            Q(vendedor__icontains=search)
            | Q(fecha__icontains=search)
        )
    page = Paginator(object_list=compras, per_page=9).get_page(page_num)

    context = {"page": page}

    return render(request=request, template_name="compra/all.html", context=context)


# VENTA
@login_required
def create_venta(request):
    # Vista para crear una venta
    if request.method == "POST":
        form = VentaForm(data=request.POST)
        if form.is_valid():
            venta = form.save()
            return redirect("select_bovinos_venta", venta_id=venta.id)
    else:
        form = VentaForm()
    return render(request, "venta/create.html", {"form": form})


@login_required
def edit_venta(request, venta_id):
    # Vista para editar una venta
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == "POST":
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            venta.save()
            return redirect("summary_venta", venta_id=venta_id)
    else:
        form = VentaForm(instance=venta)
    return render(
        request,
        "venta/edit.html",
        {"form": form, "venta_id": venta_id},
    )


@login_required
def select_bovinos_venta(request, venta_id):
    # Vista para seleccionar los bovinos a vender
    venta = get_object_or_404(Venta, id=venta_id)

    if request.method == "POST":
        form = SelectBovinosForm(request.POST)
        if form.is_valid():
            selected_bovinos = form.cleaned_data["bovinos"]
            ModifyBovinosVentaFormSet = modelformset_factory(
                Bovino, form=ModifyBovinosVentaForm, extra=0
            )
            formset = ModifyBovinosVentaFormSet(queryset=selected_bovinos)
            return render(
                request,
                "venta/modify_bovinos.html",
                {"formset": formset, "venta": venta},
            )
    else:
        form = SelectBovinosForm()

    return render(request, "venta/select_bovinos.html", {"form": form, "venta": venta})


@login_required
def modify_bovinos_venta(request, venta_id):
    # Vista para llenar los campos de la venta
    venta = get_object_or_404(Venta, id=venta_id)

    if request.method == "POST":
        ModifyBovinosVentaFormSet = modelformset_factory(
            Bovino, form=ModifyBovinosVentaForm, extra=0
        )
        formset = ModifyBovinosVentaFormSet(request.POST)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.venta = venta
                instance.save()

            return redirect("summary_venta", venta_id=venta.id)

    return redirect("select_bovinos_venta", venta_id=venta.id)


@login_required
def summary_venta(request, venta_id):
    # Vista para ver el resumen de la venta
    venta = get_object_or_404(Venta, id=venta_id)
    bovinos_vendidos = Bovino.objects.filter(venta=venta)
    precio_bovinos = (
        bovinos_vendidos.aggregate(Sum("precio_venta"))["precio_venta__sum"] or 0
    )
    ganancia_venta = precio_bovinos - venta.gastos
    return render(
        request, "venta/summary.html", {"venta": venta, "bovinos": bovinos_vendidos, "precio_bovinos": precio_bovinos, "ganancia_venta": ganancia_venta}
    )


@login_required
def all_ventas(request):
    # Página para mostrar todas las ventas
    search = request.GET.get("q")
    page_num = request.GET.get("page", 1)
    ventas = Venta.objects.all()
    if search:
        ventas = ventas.filter(
            Q(comprador__icontains=search)
            | Q(fecha__icontains=search)
        )
    page = Paginator(object_list=ventas, per_page=9).get_page(page_num)

    context = {"page": page}

    return render(request=request, template_name="venta/all.html", context=context)


# VACUNA
@login_required
def create_vacuna(request):
    if request.method == "POST":
        form = VacunaForm(data=request.POST)
        if form.is_valid():
            vacuna = form.save()
            return redirect("select_bovinos_vacuna", vacuna_id=vacuna.id)
    else:
        form = VacunaForm()
    return render(request, "vacuna/create.html", {"form": form})


@login_required
def edit_vacuna(request, vacuna_id):
    # Vista para editar una vacuna
    vacuna = get_object_or_404(Vacuna, id=vacuna_id)
    if request.method == "POST":
        form = VacunaForm(request.POST, instance=vacuna)
        if form.is_valid():
            vacuna.save()
            return redirect("summary_vacuna", vacuna_id=vacuna_id)
    else:
        form = VacunaForm(instance=vacuna)
    return render(
        request,
        "vacuna/edit.html",
        {"form": form, "vacuna_id": vacuna_id},
    )


@login_required
def select_bovinos_vacuna(request, vacuna_id):
    # Vista para seleccionar los bovinos a vacunar
    vacuna = get_object_or_404(Vacuna, id=vacuna_id)

    if request.method == "POST":
        form = SelectBovinosForm(request.POST)
        if form.is_valid():
            selected_bovinos = form.cleaned_data["bovinos"]
            VacunaBovinoFormSet = formset_factory(VacunaBovinoForm, extra=0)
            initial_data = [
                {
                    "bovino_id": bovino.id,
                    "nombre": bovino.nombre,
                    "etapa_y_edad": bovino.etapa_y_edad(),
                }
                for bovino in selected_bovinos
            ]
            formset = VacunaBovinoFormSet(initial=initial_data)
            return render(
                request,
                "vacuna/create_vacunabovino.html",
                {"formset": formset, "vacuna": vacuna},
            )
    else:
        form = SelectBovinosForm()

    return render(
        request, "vacuna/select_bovinos.html", {"form": form, "vacuna": vacuna}
    )


@login_required
def create_vacunabovino(request, vacuna_id):
    # Vista para crear la relacion entre vacuna-bovino
    vacuna = get_object_or_404(Vacuna, id=vacuna_id)

    if request.method == "POST":
        VacunaBovinoFormSet = formset_factory(VacunaBovinoForm, extra=0)
        formset = VacunaBovinoFormSet(request.POST)

        if formset.is_valid():
            try:
                for form in formset:
                    if form.is_valid():
                        vacuna_bovino = form.save(commit=False)
                        vacuna_bovino.vacuna = vacuna
                        vacuna_bovino.bovino = Bovino.objects.get(
                            id=form.cleaned_data["bovino_id"]
                        )
                        vacuna_bovino.save()

                return redirect("summary_vacuna", vacuna_id=vacuna.id)
            except ValidationError as e:
                print(f"Error de validación: {e}")
        else:
            print("Formset no válido:")
            for i, form in enumerate(formset):
                if form.errors:
                    print(f"Errores en el formulario {i}:")
                    print(form.errors)
            print("Errores del formset:")
            print(formset.errors)
            print("Errores no relacionados con formularios:")
            print(formset.non_form_errors())

    return redirect("select_bovinos_vacuna", vacuna_id=vacuna.id)


@login_required
def summary_vacuna(request, vacuna_id):
    # Vista para ver el resumen de la vacuna
    vacuna = get_object_or_404(Vacuna, id=vacuna_id)
    bovinos_vacunados = VacunaBovino.objects.filter(vacuna=vacuna)
    return render(
        request,
        "vacuna/summary.html",
        {"vacuna": vacuna, "bovinos_vacunados": bovinos_vacunados},
    )


@login_required
def all_vacunas(request):
    # Página para mostrar todas las vacunas
    search = request.GET.get("q")
    page_num = request.GET.get("page", 1)
    vacunas = Vacuna.objects.all()
    if search:
        vacunas = vacunas.filter(
            Q(vacunador__icontains=search)
            | Q(fecha__icontains=search)
        )
    page = Paginator(object_list=vacunas, per_page=9).get_page(page_num)

    context = {"page": page}

    return render(request=request, template_name="vacuna/all.html", context=context)