document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("formset-container");
    const addButton = document.getElementById("add-form");
    const totalForms = document.getElementById("id_images-TOTAL_FORMS");

    if (addButton) {
        addButton.addEventListener("click", function () {
            const currentFormCount = parseInt(totalForms.value);
            const newFormIndex = currentFormCount;

            const emptyForm = container.querySelector(".formset-row").cloneNode(true);

            emptyForm.querySelectorAll("input, select").forEach((el) => {
                if (
                    el.type === "file" ||
                    el.tagName.toLowerCase() === "select" ||
                    el.type === "text"
                ) {
                    el.value = "";
                }
                if (el.name.includes("DELETE")) {
                    el.checked = false;
                }
                if (el.name) {
                    el.name = el.name.replace(/-(\d+)-/, `-${newFormIndex}-`);
                }
                if (el.id) {
                    el.id = el.id.replace(/-(\d+)-/, `-${newFormIndex}-`);
                }
            });

            container.appendChild(emptyForm);
            totalForms.value = newFormIndex + 1;
        });
    }

    document.addEventListener("click", function (e) {
        if (e.target.closest(".delete-form")) {
            e.preventDefault();
            const row = e.target.closest(".formset-row");
            row.querySelector('input[type="hidden"][name$="-DELETE"]').value = "on";
            row.style.display = "none";
        }
    });
});
