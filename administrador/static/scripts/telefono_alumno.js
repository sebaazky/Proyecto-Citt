// Máscara y validación para el campo teléfono en crear/modificar perfil alumno (admin)
document.addEventListener("DOMContentLoaded", function () {
  var telInput = document.getElementById("id_telefono");
  if (telInput) {
    telInput.addEventListener("input", function (e) {
      let val = telInput.value;
      if (!val.startsWith("+56")) {
        val = "+56" + val.replace(/[^\d]/g, "");
      }
      let soloNumeros = val
        .replace("+56", "")
        .replace(/[^\d]/g, "")
        .slice(0, 9);
      telInput.value = "+56" + soloNumeros;
    });
    telInput.addEventListener("keydown", function (e) {
      if (
        telInput.selectionStart <= 3 &&
        (e.key === "Backspace" || e.key === "Delete")
      ) {
        e.preventDefault();
      }
    });
  }
});
