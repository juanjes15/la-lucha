from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_g, name="home_g"),
    path("bovino/create/", views.create_bovino, name="create_bovino"),
    path("bovino/<int:bovino_id>/detail/", views.detail_bovino, name="detail_bovino"),
    path("bovino/<int:bovino_id>/edit/", views.edit_bovino, name="edit_bovino"),
    path("bovino/all/", views.all_bovinos, name="all_bovinos"),
    # Compra
    path("compra/create/", views.create_compra, name="create_compra"),
    path("compra/<int:compra_id>/edit/", views.edit_compra, name="edit_compra"),
    path("compra/<int:compra_id>/bovinos/", views.create_bovinos_compra, name="create_bovinos_compra"),
    path("compra/<int:compra_id>/summary/", views.summary_compra, name="summary_compra"),
    path("compra/all/", views.all_compras, name="all_compras"),
    # Venta
    path("venta/create/", views.create_venta, name="create_venta"),
    path("venta/<int:venta_id>/edit/", views.edit_venta, name="edit_venta"),
    path("venta/<int:venta_id>/select/", views.select_bovinos_venta, name="select_bovinos_venta"),
    path("venta/<int:venta_id>/bovinos/", views.modify_bovinos_venta, name="modify_bovinos_venta"),
    path("venta/<int:venta_id>/summary/", views.summary_venta, name="summary_venta"),
    path("venta/all/", views.all_ventas, name="all_ventas"),
    # Vacuna
    path("vacuna/create/", views.create_vacuna, name="create_vacuna"),
    path("vacuna/<int:vacuna_id>/select/", views.select_bovinos_vacuna, name="select_bovinos_vacuna"),
    path("vacuna/<int:vacuna_id>/bovinos/", views.create_vacunabovino, name="create_vacunabovino"),
    path("vacuna/<int:vacuna_id>/summary/", views.summary_vacuna, name="summary_vacuna"),
    path("vacuna/all/", views.all_vacunas, name="all_vacunas"),
]
