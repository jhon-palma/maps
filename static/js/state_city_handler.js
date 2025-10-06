document.addEventListener("DOMContentLoaded", function () {
    const stateSelect = document.getElementById("id_state");
    const citySelect = document.getElementById("id_city");

    if (stateSelect && citySelect) {
        stateSelect.addEventListener("change", function () {
            const url = stateSelect.dataset.url;
            const stateId = this.value;

            fetch(`${url}?state_id=${stateId}`)
                .then((response) => response.json())
                .then((data) => {
                    citySelect.innerHTML = '<option value="">---------</option>';
                    data.forEach((city) => {
                        const option = document.createElement("option");
                        option.value = city.id;
                        option.textContent = city.name;
                        citySelect.appendChild(option);
                    });
                });
        });
    }
});
