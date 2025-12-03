// js/auth.js
export const API_BASE = "http://127.0.0.1:8080/siem/api";

console.log("auth.js cargado ✅");

// Helpers para token en localStorage
function getToken() {
  return localStorage.getItem("siem_jwt");
}
function setToken(token) {
  localStorage.setItem("siem_jwt", token);
}

// Si más adelante quieres usarlo en otras páginas, puedes exportarlos:
export { getToken, setToken };

// Función que llama al backend /auth/login
async function loginRequest(username, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    const dataErr = await res.json().catch(() => ({}));
    const msg = dataErr.error || "Credenciales inválidas";
    throw new Error(msg);
  }

  return res.json(); // { jwt: "..." }
}

// Wiring del formulario
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM listo en login.html");

  const form = document.getElementById("form-login");
  const userInput = document.getElementById("user");
  const passInput = document.getElementById("pass");
  const errorBox = document.getElementById("login-error");

  if (!form) {
    console.warn("No se encontró #login-form en esta página");
    return;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.textContent = "";

    try {
      const data = await loginRequest(userInput.value, passInput.value);
      console.log("Respuesta del backend login:", data);

      if (!data.jwt) {
        throw new Error("El servidor no devolvió JWT");
      }

      setToken(data.jwt);

      // Redirigir al dashboard
      window.location.href = "/index.html";
    } catch (err) {
      console.error("Error en login:", err);
      errorBox.textContent = err.message || "Error al iniciar sesión";
    }
  });
});
