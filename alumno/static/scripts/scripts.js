
document.addEventListener('DOMContentLoaded', function () {
    const trackButtons = document.querySelectorAll('.card .btn-primary');
    trackButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
        });
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.track-card');

    cards.forEach(card => {
        card.addEventListener('click', function () {
            this.classList.toggle('is-flipped');
        });
    });
});


//perfil

document.getElementById('nombreUsuario').addEventListener('click', function () {
    document.getElementById('perfilButton').click();
});


//img perfil
document.getElementById('uploadPhoto').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('profilePhoto').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});


//Formulario Proyecto

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('limpiarFormulario').addEventListener('click', function () {
        document.getElementById('proyectoForm').reset();
        document.getElementById('carta').value = '';
    });

    document.getElementById('crearCarta').addEventListener('click', function () {
        const nombreProyecto = document.getElementById('nombreProyecto').value;
        const responsables = document.getElementById('responsables').value;
        const track = document.getElementById('track').value;
        const recursos = document.getElementById('recursos').value;
        const alcance = document.getElementById('alcance').value;
        const objetivoPrincipal = document.getElementById('objetivoPrincipal').value;
        const objetivosSecundarios = document.getElementById('objetivosSecundarios').value;
        const beneficiarios = document.getElementById('beneficiarios').value;

        const carta = `
        Proyecto: ${nombreProyecto}
        Responsables: ${responsables}
        Track: ${track}
        Recursos Requeridos: ${recursos}
        Alcance del Proyecto: ${alcance}
        Objetivo Principal: ${objetivoPrincipal}
        Objetivos Secundarios: ${objetivosSecundarios}
        Beneficiarios: ${beneficiarios}
        `;

        document.getElementById('carta').value = carta;
    });

    // Validaciones adicionales si es necesario
});


//

