# ======================================================
# Rutas del módulo PROVEEDORES
# Incluye: Listar, Nuevo, Editar, Soft Delete + Restaurar
# ======================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Proveedor, Producto
from . import proveedores_bp   # ← IMPORTA el blueprint desde __init__.py




# ======================================================
# LISTAR PROVEEDORES (solo activos)
# ======================================================
@proveedores_bp.route("/")
def listar_proveedores():
    proveedores = Proveedor.query.filter_by(estado="activo").all()
    return render_template("proveedores/listar.html", proveedores=proveedores)


# ======================================================
# REGISTRAR NUEVO PROVEEDOR
# ======================================================
@proveedores_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():
    productos = Producto.query.filter_by(estado="activo").all()

    if request.method == "POST":
        proveedor = Proveedor(
            nombre_empresa=request.form["nombre_empresa"],
            direccion=request.form["direccion"],
            telefono=request.form["telefono"],
            persona_contacto=request.form["persona_contacto"],
            id_producto=request.form["id_producto"],
        )
        db.session.add(proveedor)
        db.session.commit()
        flash("Proveedor registrado correctamente", "success")
        return redirect(url_for("proveedores.listar_proveedores"))

    return render_template("proveedores/nuevo.html", productos=productos)


# ======================================================
# EDITAR PROVEEDOR
# ======================================================
@proveedores_bp.route("/editar/<int:id_proveedor>", methods=["GET", "POST"])
def editar_proveedor(id_proveedor):
    proveedor = Proveedor.query.get_or_404(id_proveedor)
    productos = Producto.query.filter_by(estado="activo").all()

    if request.method == "POST":
        proveedor.nombre_empresa = request.form["nombre_empresa"]
        proveedor.direccion = request.form["direccion"]
        proveedor.telefono = request.form["telefono"]
        proveedor.persona_contacto = request.form["persona_contacto"]
        proveedor.id_producto = request.form["id_producto"]

        db.session.commit()
        flash("Proveedor actualizado correctamente", "success")
        return redirect(url_for("proveedores.listar_proveedores"))

    return render_template("proveedores/editar.html", proveedor=proveedor, productos=productos)


# ======================================================
# SOFT DELETE
# ======================================================
@proveedores_bp.route("/eliminar/<int:id_proveedor>")
def eliminar_proveedor(id_proveedor):
    proveedor = Proveedor.query.get_or_404(id_proveedor)
    proveedor.estado = "inactivo"  # Soft delete
    db.session.commit()
    flash("Proveedor eliminado (Soft Delete).", "warning")
    return redirect(url_for("proveedores.listar_proveedores"))


# ======================================================
# LISTAR PROVEEDORES INACTIVOS (papelera)
# ======================================================
@proveedores_bp.route("/inactivos")
def proveedores_inactivos():
    proveedores = Proveedor.query.filter_by(estado="inactivo").all()
    return render_template("proveedores/inactivos.html", proveedores=proveedores)


# ======================================================
# RESTAURAR PROVEEDOR
# ======================================================
@proveedores_bp.route("/restaurar/<int:id_proveedor>")
def restaurar_proveedor(id_proveedor):
    proveedor = Proveedor.query.get_or_404(id_proveedor)
    proveedor.estado = "activo"
    db.session.commit()
    flash("Proveedor restaurado correctamente.", "success")
    return redirect(url_for("proveedores.proveedores_inactivos"))
