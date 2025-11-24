/**
 * ============================================================
 * MÓDULO DE COMPRAS – compras.js
 * ------------------------------------------------------------
 * Este script administra el comportamiento dinámico del 
 * formulario de registro de compras.
 *
 * Funciones principales:
 *   ✔ Autocompletar el precio unitario según proveedor elegido
 *   ✔ Mantener integridad visual con el estado cargado vía Jinja
 *   ✔ Preparar el módulo para validaciones futuras
 *   ✔ Mantener el HTML completamente limpio de lógica JS
 * ============================================================
 */

document.addEventListener("DOMContentLoaded", () => {

    // Elementos principales del formulario
    const selectProveedor = document.getElementById("proveedor");
    const inputPrecio = document.getElementById("precio_unitario_compra");

    // Si por algún motivo la vista no carga bien, evitamos fallos
    if (!selectProveedor || !inputPrecio) {
        console.warn("compras.js: Elementos no encontrados. Revisa nueva.html");
        return;
    }

    /**
     * ============================================================
     * AUTOCOMPLETAR PRECIO UNITARIO
     * ------------------------------------------------------------
     * Obtiene el precio desde el atributo:
     *     <option data-precio="X">
     *
     * Y lo asigna automáticamente al input correspondiente.
     * ============================================================
     */
    const actualizarPrecio = () => {
        const opcion = selectProveedor.selectedOptions[0];
        const precio = opcion?.getAttribute("data-precio");

        if (precio) {
            inputPrecio.value = precio;
        }
    };

    // Evento cuando el usuario selecciona un proveedor
    selectProveedor.addEventListener("change", actualizarPrecio);

    // Si la página viene recargada con un proveedor preseleccionado,
    // aseguramos que el precio también se autocompletaría.
    actualizarPrecio();
});
