from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_g, name="home_g"),
    path("bovino/create/", views.create_bovino, name="create_bovino"),
    path("bovino/<int:bovino_id>/detail/", views.detail_bovino, name="detail_bovino"),
    path("bovino/<int:bovino_id>/edit/", views.edit_bovino, name="edit_bovino"),
    # Compra
    path("compra/create/", views.create_compra, name="create_compra"),
    path("compra/<int:compra_id>/edit/", views.edit_compra, name="edit_compra"),
    path("compra/<int:compra_id>/bovinos/", views.create_bovinos_compra, name="create_bovinos_compra"),
    path("compra/<int:compra_id>/summary/", views.summary_compra, name="summary_compra"),
    # Venta
    path("venta/create/", views.create_venta, name="create_venta"),
    path("venta/<int:venta_id>/select/", views.select_bovinos_venta, name="select_bovinos_venta"),
    path("venta/<int:venta_id>/bovinos/", views.modify_bovinos_venta, name="modify_bovinos_venta"),
    path("venta/<int:venta_id>/summary/", views.summary_venta, name="summary_venta"),
    # Vacuna
    path("vacuna/create/", views.create_vacuna, name="create_vacuna"),
    path("vacuna/<int:vacuna_id>/select/", views.select_bovinos_vacuna, name="select_bovinos_vacuna"),
    path("vacuna/<int:vacuna_id>/bovinos/", views.create_vacunabovino, name="create_vacunabovino"),
    path("vacuna/<int:vacuna_id>/summary/", views.summary_vacuna, name="summary_vacuna"),
]
