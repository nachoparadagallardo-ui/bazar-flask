# ======================================================
# Rutas del módulo PRODUCTOS
# Incluye: CRUD + Soft Delete + Restauración
# ======================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Producto
from . import productos_bp

# ======================================================
# LISTAR PRODUCTOS ACTIVOS
# ======================================================
@productos_bp.route("/")
def listar_productos():
    productos = Producto.query.filter_by(estado="activo").all()
    return render_template("productos/listar.html", productos=productos)

# =======================================================
# LISTAR PRODUCTOS INACTIVOS
# =======================================================
@productos_bp.route("/inactivos")
def productos_inactivos():
    productos = Producto.query.filter_by(estado="inactivo").all()
    return render_template("productos/inactivos.html", productos=productos)

# =======================================================
# RESTAURAR PRODUCTO
# =======================================================
@productos_bp.route("/restaurar/<int:id_producto>")
def restaurar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    producto.estado = "activo"
    db.session.commit()

    flash("Producto restaurado correctamente.", "success")
    return redirect(url_for("productos.productos_inactivos"))

# ======================================================
# REGISTRAR NUEVO PRODUCTO
# ======================================================
@productos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    if request.method == "POST":
        producto = Producto(
            nombre=request.form["nombre"],
            tipo=request.form["tipo"],
            cantidad=request.form["cantidad"],
            fecha_ingreso=request.form["fecha_ingreso"],
            marca=request.form["marca"],
            precio_unitario_venta=request.form["precio_unitario_venta"],
            precio_unitario_compra=request.form["precio_unitario_compra"]
        )

        db.session.add(producto)
        db.session.commit()
        flash("Producto registrado correctamente", "success")
        return redirect(url_for("productos.listar_productos"))

    return render_template("productos/nuevo.html")

# ======================================================
# EDITAR PRODUCTO
# ======================================================
@productos_bp.route("/editar/<int:id_producto>", methods=["GET", "POST"])
def editar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)

    if request.method == "POST":
        producto.nombre = request.form.get("nombre")
        producto.tipo = request.form.get("tipo")
        producto.cantidad = request.form.get("cantidad")
        producto.marca = request.form.get("marca")
        producto.precio_unitario_venta = request.form.get("precio_unitario_venta")
        producto.precio_unitario_compra = request.form.get("precio_unitario_compra")

        db.session.commit()
        flash("Producto editado correctamente", "success")
        return redirect(url_for("productos.listar_productos"))

    return render_template("productos/editar.html", producto=producto)

# ======================================================
# SOFT DELETE (NO elimina físicamente)
# ======================================================
@productos_bp.route("/eliminar/<int:id_producto>")
def eliminar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    producto.estado = "inactivo"
    db.session.commit()

    flash("Producto desactivado (Soft Delete)", "warning")
    return redirect(url_for("productos.listar_productos"))
