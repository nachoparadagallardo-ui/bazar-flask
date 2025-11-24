# ================================================
# RUTAS DEL MÓDULO VENTAS
# ================================================

from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from extensions import db
from models import Venta, DetalleVenta, Producto
from . import ventas_bp


# =======================================================
# LISTAR VENTAS ACTIVAS
# =======================================================
@ventas_bp.route("/")
def listar_ventas():
    ventas = Venta.query.filter_by(estado="activo").all()
    return render_template("ventas/listar.html", ventas=ventas)


# =======================================================
# LISTAR VENTAS INACTIVAS
# =======================================================
@ventas_bp.route("/inactivas")
def ventas_inactivas():
    ventas = Venta.query.filter_by(estado="inactivo").all()
    return render_template("ventas/inactivas.html", ventas=ventas)


# =======================================================
# REGISTRAR NUEVA VENTA CON VALIDACIÓN COMPLETA
# =======================================================
@ventas_bp.route("/nueva", methods=["GET", "POST"])
def nueva_venta():

    productos = Producto.query.filter_by(estado="activo").all()

    if request.method == "POST":

        # Capturar líneas dinámicas
        indices = []
        for key in request.form:
            if key.startswith("producto_"):
                indices.append(key.split("_")[1])
        indices = sorted(set(indices))

        lineas = []

        # ===============================
        # VALIDAR STOCK DE CADA LÍNEA
        # ===============================
        for i in indices:

            id_producto = request.form.get(f"producto_{i}")
            cantidad = request.form.get(f"cantidad_{i}")
            precio = request.form.get(f"precio_{i}")
            subtotal = request.form.get(f"subtotal_{i}")

            if not id_producto or not cantidad:
                continue  # ignorar filas vacías

            cantidad = int(cantidad)
            precio = float(precio)
            subtotal = float(subtotal) if subtotal else cantidad * precio

            producto = Producto.query.get(int(id_producto))

            if not producto:
                flash("Producto inexistente.", "danger")
                return redirect(url_for("ventas.nueva_venta"))

            if producto.cantidad < cantidad:
                flash(
                    f"Stock insuficiente para '{producto.nombre}'. "
                    f"Stock disponible: {producto.cantidad}",
                    "danger"
                )
                return redirect(url_for("ventas.nueva_venta"))

            lineas.append({
                "producto": producto,
                "id_producto": producto.id_producto,
                "cantidad": cantidad,
                "precio": precio,
                "subtotal": subtotal
            })

        # Ninguna línea válida
        if not lineas:
            flash("Debe ingresar al menos un producto válido.", "warning")
            return redirect(url_for("ventas.nueva_venta"))

        # ===============================
        # CREAR LA VENTA (YA VALIDADA)
        # ===============================
        venta = Venta(
            fecha=datetime.now(),
            total=0,
            estado="activo"
        )
        db.session.add(venta)
        db.session.flush()

        total_venta = 0

        # Guardar detalles
        for l in lineas:

            det = DetalleVenta(
                id_venta=venta.id_venta,
                id_producto=l["id_producto"],
                cantidad=l["cantidad"],
                precio_unitario=l["precio"],
                subtotal=l["subtotal"]
            )
            db.session.add(det)

            # Descontar stock
            l["producto"].cantidad -= l["cantidad"]

            total_venta += l["subtotal"]

        venta.total = total_venta

        db.session.commit()

        flash("Venta registrada correctamente.", "success")
        return redirect(url_for("ventas.listar_ventas"))

    # GET
    return render_template("ventas/nueva.html", productos=productos)


# =======================================================
# ELIMINAR (SOFT DELETE)
# =======================================================
@ventas_bp.route("/eliminar/<int:id_venta>")
def eliminar_venta(id_venta):
    venta = Venta.query.get_or_404(id_venta)
    venta.estado = "inactivo"
    db.session.commit()
    flash("La venta fue eliminada correctamente.", "success")
    return redirect(url_for("ventas.listar_ventas"))


# =======================================================
# RESTAURAR VENTA
# =======================================================
@ventas_bp.route("/restaurar/<int:id_venta>")
def restaurar_venta(id_venta):
    venta = Venta.query.get_or_404(id_venta)
    venta.estado = "activo"
    db.session.commit()
    flash("La venta fue restaurada correctamente.", "success")
    return redirect(url_for("ventas.ventas_inactivas"))
