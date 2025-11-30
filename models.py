# ========================================================================
# MODELOS SQLAlchemy para el sistema de Gestión de Bazar
# ========================================================================

from datetime import datetime, timedelta, timezone
from extensions import db

# Zona horaria de Chile (UTC-3)
tz_chile = timezone(timedelta(hours=-3))

# ========================================================================
# TABLA: PRODUCTO
# ========================================================================
class Producto(db.Model):
    __tablename__ = "producto"

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)  # Stock actual
    fecha_ingreso = db.Column(db.Date, default=datetime.utcnow)
    marca = db.Column(db.String(50), nullable=False)

    precio_unitario_venta = db.Column(db.Numeric(10, 2), nullable=False)
    precio_unitario_compra = db.Column(db.Numeric(10, 2), nullable=False)

    estado = db.Column(db.String(20), default="activo")  # Soft delete

    # Relaciones
    proveedores = db.relationship("Proveedor", back_populates="producto")
    detalles_venta = db.relationship("DetalleVenta", back_populates="producto")


# ========================================================================
# TABLA: PROVEEDOR                                                                                                                                    
# ========================================================================
class Proveedor(db.Model):
    __tablename__ = "proveedor"

    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    persona_contacto = db.Column(db.String(100), nullable=False)

    id_producto = db.Column(db.Integer, db.ForeignKey("producto.id_producto"), nullable=False)
    producto = db.relationship("Producto", back_populates="proveedores")

    compras = db.relationship("Compra", back_populates="proveedor")

    estado = db.Column(db.String(20), default="activo")


# ========================================================================
# TABLA: COMPRA                                                                                 
# ========================================================================
class Compra(db.Model):
    __tablename__ = "compra"

    id_compra = db.Column(db.Integer, primary_key=True)

    # Fecha completa (fecha + hora chilena)
    fecha = db.Column(
        db.DateTime,
        default=lambda: datetime.now(tz_chile),
        nullable=False
    )

    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario_compra = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    id_proveedor = db.Column(db.Integer, db.ForeignKey("proveedor.id_proveedor"), nullable=False)
    proveedor = db.relationship("Proveedor", back_populates="compras")

    estado = db.Column(db.String(20), default="activo")  # Soft delete


# ========================================================================
# TABLA: VENTA
# Representa cada venta con su fecha y hora exacta (UTC-3)
# ========================================================================
class Venta(db.Model):
    __tablename__ = "venta"

    id_venta = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(
        db.DateTime,
        default=lambda: datetime.now(tz_chile),
        nullable=False
    )

    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(20), default="activo")

    # Relación con detalles de venta
    detalles = db.relationship(
        "DetalleVenta",
        back_populates="venta",
        cascade="all, delete"
    )


# ========================================================================
# TABLA: DETALLEVENTA
# Almacena cada producto incluido en una venta                                                                    
# ========================================================================
class DetalleVenta(db.Model):
    __tablename__ = "detalleventa"

    id_detalle = db.Column(db.Integer, primary_key=True)

    id_venta = db.Column(db.Integer, db.ForeignKey("venta.id_venta"), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey("producto.id_producto"), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    venta = db.relationship("Venta", back_populates="detalles")
    producto = db.relationship("Producto", back_populates="detalles_venta")
