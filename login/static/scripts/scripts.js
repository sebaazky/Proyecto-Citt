(function () {
  "use strict";

  var form = document.querySelector(".needs-validation");
  var correo = document.getElementById("correo");
  var usuario = document.getElementById("usuario");
  var password1 = document.getElementById("password1");
  var password2 = document.getElementById("password2");

  form.addEventListener(
    "submit",
    function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }

      // Validar que las contraseñas coincidan
      if (password1.value !== password2.value) {
        password2.setCustomValidity("Las contraseñas no coinciden.");
        password2.classList.add("is-invalid");
      } else {
        password2.setCustomValidity("");
        password2.classList.remove("is-invalid");
      }

      form.classList.add("was-validated");
    },
    false
  );

  // Event listeners para quitar los estilos de invalid-feedback
  correo.addEventListener(
    "input",
    function () {
      correo.setCustomValidity("");
      correo.classList.remove("is-invalid");
    },
    false
  );

  usuario.addEventListener(
    "input",
    function () {
      usuario.setCustomValidity("");
      usuario.classList.remove("is-invalid");
    },
    false
  );

  password1.addEventListener(
    "input",
    function () {
      // Limpiar la validación y los estilos de invalid-feedback
      password1.setCustomValidity("");
      password1.classList.remove("is-invalid");
    },
    false
  );

  password2.addEventListener(
    "input",
    function () {
      // Limpiar la validación y los estilos de invalid-feedback
      password2.setCustomValidity("");
      password2.classList.remove("is-invalid");
    },
    false
  );

  // Mantener los datos ingresados si el formulario es inválido
  form.addEventListener(
    "invalid",
    function (event) {
      event.preventDefault();
      form.classList.add("was-validated");
    },
    true
  );

  // Mantener los datos ingresados si el formulario es válido
  form.addEventListener("input", function (event) {
    if (event.target.tagName.toLowerCase() === "input") {
      event.target.classList.remove("is-invalid");
    }
  });
})();
