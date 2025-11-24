from flask import render_template
from models import Compra, Venta
from datetime import datetime, time
from extensions import db
from . import balance_bp
from sqlalchemy import func
from decimal import Decimal
import pytz    # Manejo seguro de zona horaria

# ------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------------------

IVA = Decimal("0.10")                     # IVA descontado (10%)
tz = pytz.timezone("America/Santiago")    # Zona horaria local de Chile


# ------------------------------------------------------------
# FUNCIÓN PRINCIPAL DE CÁLCULO
# Recibe un rango datetime completo (inicio y fin).
# Retorna totales de compras, ventas, IVA y ganancias.
# ------------------------------------------------------------
def calcular_balance(inicio_dt, fin_dt):

    # Total de compras en el rango
    total_compras = db.session.query(
        func.coalesce(func.sum(Compra.total), 0)
    ).filter(
        Compra.fecha >= inicio_dt,
        Compra.fecha <= fin_dt
    ).scalar()

    # Total de ventas en el rango
    total_ventas = db.session.query(
        func.coalesce(func.sum(Venta.total), 0)
    ).filter(
        Venta.fecha >= inicio_dt,
        Venta.fecha <= fin_dt
    ).scalar()

    # Cálculos financieros
    ganancia_bruta = total_ventas - total_compras
    iva_descuento = ganancia_bruta * IVA
    ganancia_neta = ganancia_bruta - iva_descuento

    return {
        "total_compras": total_compras,
        "total_ventas": total_ventas,
        "ganancia_bruta": ganancia_bruta,
        "iva_descuento": iva_descuento,
        "ganancia_neta": ganancia_neta,
    }


# ------------------------------------------------------------
# BALANCE DIARIO
# Toma solo las operaciones del día actual completo
# (00:00:00 → 23:59:59)
# ------------------------------------------------------------
@balance_bp.route("/diario")
def balance_diario():

    hoy = datetime.now(tz).date()

    # Rango temporal completo del día
    inicio_dt = datetime.combine(hoy, time.min).astimezone(tz)
    fin_dt    = datetime.combine(hoy, time.max).astimezone(tz)

    datos = calcular_balance(inicio_dt, fin_dt)

    return render_template("balance/diario.html", datos=datos, fecha=hoy)


# ------------------------------------------------------------
# BALANCE MENSUAL
# Desde el primer día del mes → día actual (rango completo)
# ------------------------------------------------------------
@balance_bp.route("/mensual")
def balance_mensual():

    hoy = datetime.now(tz)

    # Primer día del mes como date
    inicio_mes = hoy.replace(day=1).date()

    # Rango temporal completo del mes
    inicio_dt = datetime.combine(inicio_mes, time.min).astimezone(tz)
    fin_dt    = datetime.combine(hoy.date(), time.max).astimezone(tz)

    datos = calcular_balance(inicio_dt, fin_dt)

    return render_template("balance/mensual.html", datos=datos, fecha=inicio_mes)
