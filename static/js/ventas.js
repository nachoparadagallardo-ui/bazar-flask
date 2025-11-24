// ==========================================================
//  MÓDULO DE VENTAS - CONTROL DE DETALLES
// ==========================================================

// 1) AGREGAR UNA NUEVA FILA DE PRODUCTO
document.addEventListener("DOMContentLoaded", () => {

    const btnAgregar = document.getElementById("agregar-fila"); // botón para agregar fila
    const tbody = document.getElementById("tbody-detalle");     // cuerpo de la tabla de detalles

    btnAgregar.addEventListener("click", () => {   // al hacer clic en "Agregar Fila"

        const last = tbody.querySelector("tr:last-child"); // última fila existente
        const newIndex = Number(last.dataset.index) + 1; // nuevo índice

        // Clonar la última fila

        const clone = last.cloneNode(true); // clonar la última fila
        clone.dataset.index = newIndex; // actualizar el índice del dataset

        // Renombrar inputs
        clone.querySelector("[name^='producto_']").name = `producto_${newIndex}`;
        clone.querySelector("[name^='cantidad_']").name = `cantidad_${newIndex}`;
        clone.querySelector("[name^='precio_']").name = `precio_${newIndex}`;
        clone.querySelector("[name^='subtotal_']").name = `subtotal_${newIndex}`;

        // Reset valores
        clone.querySelector("select").selectedIndex = 0;
        clone.querySelectorAll("input").forEach(i => i.value = "");

        // Eliminar mensaje de stock si existe
        const msg = clone.querySelector(".mensaje-stock");
        if (msg) msg.remove();

        tbody.appendChild(clone);
    });

    // ==========================================================
    // 2) ELIMINAR UNA FILA DE PRODUCTO
    // ==========================================================
    document.addEventListener("click", e => {
        if (e.target.classList.contains("eliminar-fila")) {

            const filas = document.querySelectorAll("#tbody-detalle tr");

            if (filas.length > 1) {
                e.target.closest("tr").remove();
                actualizarTotal();
            }
        }
    });

    // ==========================================================
    // 3) CÁLCULO DINÁMICO DE SUBTOTALES Y TOTAL
    // ==========================================================
    document.addEventListener("input", e => {

        const tr = e.target.closest("tr");

        // Si cambia la cantidad o el precio → actualizar subtotal
        if (e.target.name.startsWith("cantidad") || e.target.name.startsWith("precio")) {

            const cantidad = parseFloat(tr.querySelector("[name^='cantidad_']").value) || 0;
            const precio = parseFloat(tr.querySelector("[name^='precio_']").value) || 0;

            tr.querySelector("[name^='subtotal_']").value = (cantidad * precio).toFixed(2);

            actualizarTotal();
        }

        // ------------------------------------------------------
        // VALIDACIÓN DE STOCK
        // ------------------------------------------------------
        if (e.target.name.startsWith("cantidad_")) {

            const select = tr.querySelector("select");
            const stock = parseInt(select.options[select.selectedIndex].dataset.stock || 0);

            const cantidadIngresada = parseInt(e.target.value || 0);

            let msg = tr.querySelector(".mensaje-stock");

            if (cantidadIngresada > stock) {

                e.target.classList.add("is-invalid");

                if (!msg) {
                    msg = document.createElement("div");
                    msg.classList.add("mensaje-stock", "text-danger", "mt-1", "fw-bold");
                    msg.textContent = `❌ Stock insuficiente. Máximo disponible: ${stock}`;
                    tr.cells[1].appendChild(msg);
                }

            } else {
                e.target.classList.remove("is-invalid");
                if (msg) msg.remove();
            }
        }
    });

    // ==========================================================
    // FUNCION PARA CALCULAR TOTAL GENERAL
    // ==========================================================
    function actualizarTotal() {
        let total = 0;

        document.querySelectorAll("[name^='subtotal_']").forEach(s => {
            total += parseFloat(s.value) || 0;
        });

        document.getElementById("total").value = total.toFixed(2);
    }

    // ==========================================================
    // VALIDACIÓN FINAL DEL FORMULARIO
    // ==========================================================
    window.validarFormulario = function() {

        const filas = document.querySelectorAll("#tbody-detalle tr");

        for (let tr of filas) {

            const select = tr.querySelector("select");
            const cantidadInput = tr.querySelector("[name^='cantidad_']");
            const precio = tr.querySelector("[name^='precio_']").value;

            const stock = parseInt(select.options[select.selectedIndex].dataset.stock || 0);
            const cantidad = parseInt(cantidadInput.value || 0);

            if (select.value === "" || cantidadInput.value === "" || precio === "") {
                alert("Hay filas incompletas. Por favor revise el formulario.");
                return false;
            }

            if (cantidad > stock) {
                alert(`El producto "${select.options[select.selectedIndex].text}" no tiene suficiente stock.`);
                cantidadInput.classList.add("is-invalid");
                return false;
            }
        }

        return true; // todo OK
    };

}); // FIN DOMContentLoaded
