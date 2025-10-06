    document.addEventListener("DOMContentLoaded", function () {
        // ------------------------------
        // 1. Estado → Ciudades (AJAX)
        // ------------------------------
        const stateSelect = document.getElementById("id_state");
        const citySelect = document.getElementById("id_city");

        if (stateSelect && citySelect) {
            stateSelect.addEventListener("change", function () {
                const url = stateSelect.dataset.url;
                const stateId = this.value;

                fetch(`${url}?state_id=${stateId}`)
                    .then(response => response.json())
                    .then(data => {
                        citySelect.innerHTML = '<option value="">---------</option>';
                        data.forEach(city => {
                            const option = document.createElement("option");
                            option.value = city.id;
                            option.textContent = city.name;
                            citySelect.appendChild(option);
                        });
                    });
            });
        }

        // ------------------------------
        // 2. Tipo de contribuyente → Tipo de identificador
        // ------------------------------
        const typeContributor = document.getElementById("id_type_contributor");
        const typeIdentifier = document.getElementById("id_type_identifier");
        const name = document.getElementById("id_name");

        function setIdentifier() {
            if (typeContributor && typeContributor.value === "1") { // Persona Jurídica
                typeIdentifier.value = "31";  // NIT
                typeIdentifier.setAttribute("readonly", "readonly");
                name.setAttribute("required", "required");
            } else {
                typeIdentifier.removeAttribute("readonly");
                name.removeAttribute("required", "required");
            }
        }

        if (typeContributor && typeIdentifier) {
            setIdentifier();
            typeContributor.addEventListener("change", setIdentifier);
        }

        // ------------------------------
        // 3. Calcular DV a partir del NIT
        // ------------------------------
        const nitInput = document.getElementById("id_document_number");
        const dvInput = document.getElementById("id_dv");

        const multiplicadores = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71];

        function calcularDV(nit) {
            nit = nit.replace(/[^\d]/g, "");
            if (nit.length < 2) return "";
            nit = nit.split("").reverse().join("");
            let suma = 0;
            for (let i = 0; i < nit.length; i++) {
                suma += parseInt(nit[i]) * multiplicadores[i];
            }
            const residuo = suma % 11;
            return (residuo === 0 || residuo === 1) ? residuo : 11 - residuo;
        }

        if (nitInput && dvInput) {
            nitInput.addEventListener("input", function () {
                const dv = calcularDV(nitInput.value);
                if (dv !== "") dvInput.value = dv;
            });
        }

        // ------------------------------
        // 4. Mostrar/Ocultar campos Persona Natural
        // ------------------------------
        const naturalFields = document.querySelectorAll(".natural-fields");

        function toggleFields() {
            if (typeContributor && typeContributor.value === "2") { // Persona Natural
                naturalFields.forEach(field => {
                    field.style.display = "flex";
                    field.querySelectorAll("input, select, textarea").forEach(input => {
                        input.removeAttribute("disabled");
                        if (input.id === "id_first_name" || input.id === "id_first_last_name") {
                            input.setAttribute("required", "required");
                        }
                    });
                });
            } else { // Persona Jurídica
                naturalFields.forEach(field => {
                    field.style.display = "none";
                    field.querySelectorAll("input, select, textarea").forEach(input => {
                        input.setAttribute("disabled", "disabled");
                        input.removeAttribute("required");
                        input.value = "";
                    });
                });
            }
        }

        if (typeContributor) {
            toggleFields();
            typeContributor.addEventListener("change", toggleFields);
        }
        // ------------------------------
        // 5. Validar DV solo números (máx 1 dígito)
        // ------------------------------
        if (dvInput) {
            dvInput.addEventListener("input", function () {
                this.value = this.value.replace(/[^0-9]/g, "").slice(0, 1);
            });
        }

        document.querySelectorAll("input[type='number']").forEach(function (el) {
            el.addEventListener("keypress", function (evt) {
                // Solo permitir números, punto y coma (para decimales)
                if (!/[0-9.,]/.test(evt.key)) {
                    evt.preventDefault();
                }
            });
        });
    });
