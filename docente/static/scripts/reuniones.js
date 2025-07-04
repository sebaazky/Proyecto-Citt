// Validaciones y lógica para formularios de reuniones (docente)
function getToday() {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, "0");
  const dd = String(today.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function toggleReunionFields(uid) {
  const modalidad = document.getElementById("modalidad" + uid);
  const linkInput = document.getElementById("link_virtual" + uid);
  const ubicacionInput = document.getElementById("ubicacion" + uid);
  if (!modalidad || !linkInput || !ubicacionInput) return;
  if (modalidad.value === "virtual") {
    linkInput.disabled = false;
    linkInput.required = true;
    ubicacionInput.disabled = true;
    ubicacionInput.required = false;
    ubicacionInput.value = "-";
  } else {
    ubicacionInput.disabled = false;
    ubicacionInput.required = true;
    linkInput.disabled = true;
    linkInput.required = false;
    linkInput.value = "-";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Para selects de modalidad
  document.querySelectorAll(".modalidad-select").forEach(function (select) {
    const uid = select.getAttribute("data-uid") || "";
    select.addEventListener("change", function () {
      toggleReunionFields(uid);
    });
    toggleReunionFields(uid);
  });
  // Validación de fechas: no permitir fechas anteriores a hoy
  var hoy = getToday();
  document.querySelectorAll(".fecha-reunion").forEach(function (input) {
    input.setAttribute("min", hoy);
    input.addEventListener("input", function () {
      if (input.value < hoy) {
        input.setCustomValidity(
          "No puedes seleccionar una fecha anterior a hoy."
        );
      } else {
        input.setCustomValidity("");
      }
    });
  });
});
