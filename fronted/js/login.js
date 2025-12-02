export const API_BASE = "http://127.0.0.1:8080/siem/api";


document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-login");
  const errorBox = document.getElementById("login-error");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.style.display = "none";
    errorBox.textContent = "";

    const username = document.getElementById("user").value.trim();
    const password = document.getElementById("pass").value;

    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        errorBox.textContent = data.error || "Credenciales inválidas";
        errorBox.style.display = "block";
        return;
      }

      // Guardar JWT en localStorage
      localStorage.setItem("siem_jwt", data.token);

      // Redirigir al dashboard principal
      window.location.href = "index.html";
    } catch (err) {
      console.error("Error en login:", err);
      errorBox.textContent = "Error de conexión con el backend";
      errorBox.style.display = "block";
    }
  });
});
