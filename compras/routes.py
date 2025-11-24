# ==========================================
#   COMPRAS: rutas del módulo de compras
# ==========================================

from flask import render_template, request, redirect, url_for, flash # ✔ Importa funciones de Flask necesarias
from extensions import db # ✔ Importa la extensión de base de datos
from models import Compra, Proveedor, Producto #Importa los modelos necesarios para las operaciones de compras
from . import compras_bp   # ✔ Importa el blueprint registrado en __init__.py


# ==========================================
# LISTAR COMPRAS ACTIVAS
# ==========================================
@compras_bp.route("/") #Establece la ruta principal del módulo compras
def listar_compras(): #Define la función para listar las compras y mostrar la plantilla correspondiente
    """
    Muestra todas las compras activas (estado = activo)   
    """
    compras = Compra.query.filter_by(estado="activo").all()  #Ejecuta la consulta para obtener todas las compras activas
    return render_template("compras/listar.html", compras=compras) #ReTorna el resultado a la plantilla listar.html y pasa las compras obtenidas


# ==========================================
# REGISTRAR COMPRA
# ==========================================
@compras_bp.route("/nueva", methods=["GET", "POST"])
def nueva_compra():

    proveedores = (
        Proveedor.query.filter_by(estado="activo")
        .join(Producto)
        .add_columns(
            Proveedor.id_proveedor,
            Proveedor.nombre_empresa,
            Proveedor.id_producto,
            Producto.precio_unitario_compra,
        )
    )

    id_proveedor = request.args.get("id_proveedor", type=int)
    producto = None
    if id_proveedor:
        proveedor = Proveedor.query.get(id_proveedor)
        if proveedor:
            producto = Producto.query.get(proveedor.id_producto)

    if request.method == "POST":

        id_proveedor = request.form.get("id_proveedor")
        cantidad = request.form.get("cantidad")
        precio = request.form.get("precio_unitario_compra")

        if not id_proveedor or not cantidad or not precio:
            flash("Debes completar todos los campos.", "danger")
            return redirect(url_for("compras.nueva_compra"))

        total = float(cantidad) * float(precio)

        # Crear compra
        compra = Compra(
            id_proveedor=id_proveedor,
            cantidad=cantidad,
            precio_unitario_compra=precio,
            total=total
        )

        db.session.add(compra)

        # ==============================================
        # AUMENTAR STOCK DEL PRODUCTO ASOCIADO
        # ==============================================
        proveedor = Proveedor.query.get(id_proveedor)
        producto = Producto.query.get(proveedor.id_producto)

        producto.cantidad += int(cantidad)

        # ==============================================

        db.session.commit()

        flash("Compra registrada correctamente", "success")
        return redirect(url_for("compras.listar_compras"))

    return render_template(
        "compras/nueva.html",
        proveedores=proveedores,
        producto=producto,
        id_proveedor=id_proveedor
    )



# ==========================================
# LISTAR COMPRAS INACTIVAS (PAPELERA)
# ==========================================
@compras_bp.route("/papelera")
def compras_inactivas():
    """
    Muestra compras con estado = inactivo
    """
    compras = Compra.query.filter_by(estado="inactivo").all()
    return render_template("compras/papelera.html", compras=compras)


# ==========================================
# SOFT DELETE
# ==========================================
@compras_bp.route("/eliminar/<int:id_compra>")
def eliminar_compra(id_compra):
    """
    Soft Delete: no elimina registro, solo cambia estado
    """
    compra = Compra.query.get_or_404(id_compra)
    compra.estado = "inactivo"
    db.session.commit()

    flash("Compra eliminada (enviada a papelera)", "warning")
    return redirect(url_for("compras.listar_compras"))


# ==========================================
# RESTAURAR COMPRA
# ==========================================
@compras_bp.route("/restaurar/<int:id_compra>")
def restaurar_compra(id_compra):
    """
    Restaura compra desde la papelera (estado = activo)
    """
    compra = Compra.query.get_or_404(id_compra)
    compra.estado = "activo"
    db.session.commit()

    flash("Compra restaurada correctamente", "success")
    return redirect(url_for("compras.compras_inactivas"))
