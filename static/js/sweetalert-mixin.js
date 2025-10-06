const SweetAlertFormMixin = {
    initConfirm: function(formId, options = {}) {
        const form = document.getElementById(formId);
        if (!form) return;

        form.addEventListener("submit", function(e) {
            e.preventDefault();

            Swal.fire({
                title: options.title || '¿Estás seguro?',
                text: options.text || 'Se procederá a guardar la información.',
                icon: options.icon || 'question',
                showCancelButton: true,
                confirmButtonText: options.confirmText || 'Sí, continuar',
                cancelButtonText: options.cancelText || 'Cancelar',
                customClass: {
                    confirmButton: 'btn btn-success px-5',  
                    cancelButton: 'btn btn-danger px-5'
                },
            }).then((result) => {
                if (result.isConfirmed) {
                    Swal.fire({
                        title: options.loadingTitle || 'Procesando...',
                        text: options.loadingText || 'Por favor espera',
                        allowOutsideClick: false,
                        allowEscapeKey: false,
                        didOpen: () => {
                            Swal.showLoading();
                        }
                    });

                    form.submit();
                }
            });
        });
    }
};
