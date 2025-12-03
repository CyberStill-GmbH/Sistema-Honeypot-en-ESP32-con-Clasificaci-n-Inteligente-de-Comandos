const API_BASE = "http://127.0.0.1:8080/siem/api";

function getToken() {
  return localStorage.getItem("siem_jwt");
}

// Proteger la página: si no hay token, vuelve al login
if (!getToken()) {
  window.location.href = "/login.html";
}

async function loadTokens() {
  const tbody = document.querySelector("#tbl-tokens tbody");
  const emptyMsg = document.getElementById("tokens-empty");

  tbody.innerHTML = "";
  emptyMsg.style.display = "none";

  try {
    const res = await fetch(`${API_BASE}/tokens`, {
      headers: {
        "Authorization": `Bearer ${getToken()}`
      }
    });

    if (!res.ok) {
      console.error("Error HTTP al obtener tokens:", res.status);
      emptyMsg.textContent = "No se pudo obtener la lista de tokens.";
      emptyMsg.style.display = "block";
      return;
    }

    const data = await res.json();
    const tokens = data.tokens || data || [];

    if (tokens.length === 0) {
      emptyMsg.textContent = "No hay tokens registrados.";
      emptyMsg.style.display = "block";
      return;
    }

    for (const t of tokens) {
      const tr = document.createElement("tr");

      const tokenMask = t.token
        ? t.token.slice(0, 8) + "..." + t.token.slice(-4)
        : "";

      const activo = t.active ? "Sí" : "No";

      tr.innerHTML = `
        <td>${t.id}</td>
        <td><code>${tokenMask}</code></td>
        <td>${t.owner || ""}</td>
        <td>${activo}</td>
        <td>${t.created_at || ""}</td>
        <td>
          <button class="btn btn-sm btn-outline-warning btn-toggle" data-id="${t.id}">
            ${t.active ? "Desactivar" : "Activar"}
          </button>
          <button class="btn btn-sm btn-outline-danger btn-delete" data-id="${t.id}">
            Eliminar
          </button>
        </td>
      `;

      tbody.appendChild(tr);
    }

    // Toggle activo
    tbody.querySelectorAll(".btn-toggle").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-id");
        const row = btn.closest("tr");
        const current = row.children[3].textContent.trim() === "Sí";
        const newActive = !current;

        try {
          const resPatch = await fetch(`${API_BASE}/tokens/${id}`, {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify({ active: newActive })
          });

          if (!resPatch.ok) {
            alert("No se pudo actualizar el token.");
            return;
          }

          loadTokens();
        } catch (err) {
          console.error("Error al actualizar token:", err);
          alert("Error de conexión al actualizar.");
        }
      });
    });

    // Eliminar token
    tbody.querySelectorAll(".btn-delete").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-id");
        if (!confirm(`¿Eliminar token ${id}?`)) return;

        try {
          const resDel = await fetch(`${API_BASE}/tokens/${id}`, {
            method: "DELETE",
            headers: {
              "Authorization": `Bearer ${getToken()}`
            }
          });

          if (!resDel.ok) {
            alert("No se pudo eliminar el token.");
            return;
          }

          loadTokens();
        } catch (err) {
          console.error("Error al eliminar token:", err);
          alert("Error de conexión al eliminar.");
        }
      });
    });

  } catch (err) {
    console.error("Error cargando tokens:", err);
    emptyMsg.textContent = "Error de conexión al obtener tokens.";
    emptyMsg.style.display = "block";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const btnLogout = document.getElementById("btn-logout");
  if (btnLogout) {
    btnLogout.addEventListener("click", () => {
      localStorage.removeItem("siem_jwt");
      window.location.href = "/login.html";
    });
  }

  const form = document.getElementById("form-token");
  const msgCreated = document.getElementById("token-created");
  const btnRefresh = document.getElementById("btn-refresh");

  if (btnRefresh) {
    btnRefresh.addEventListener("click", () => {
      loadTokens();
    });
  }

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      msgCreated.style.display = "none";
      msgCreated.textContent = "";

      const owner = document.getElementById("owner").value.trim();
      if (!owner) return;

      try {
        const res = await fetch(`${API_BASE}/tokens`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
          },
          body: JSON.stringify({ owner })
        });

        const data = await res.json();

        if (!res.ok) {
          alert(data.error || "No se pudo crear el token.");
          return;
        }

        msgCreated.textContent = `Token creado: ${data.token || "(ver en tabla)"}`;
        msgCreated.style.display = "block";

        form.reset();
        loadTokens();
      } catch (err) {
        console.error("Error al crear token:", err);
        alert("Error de conexión al crear token.");
      }
    });
  }

  // Cargar tokens al inicio
  loadTokens();
});
