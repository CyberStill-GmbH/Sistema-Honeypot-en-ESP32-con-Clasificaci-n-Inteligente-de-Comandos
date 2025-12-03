const API_BASE = "http://127.0.0.1:8080/siem/api";

function getToken() {
  return localStorage.getItem("siem_jwt");
}

// Proteger la página: si no hay token, vuelve al login
if (!getToken()) {
  window.location.href = "/login.html";
}

async function loadEvents() {
  const tbody = document.querySelector("#tbl-events tbody");
  const emptyMsg = document.getElementById("events-empty");

  tbody.innerHTML = "";
  emptyMsg.style.display = "none";

  try {
    const res = await fetch(`${API_BASE}/events?limit=100&offset=0`, {
      headers: {
        "Authorization": `Bearer ${getToken()}`
      }
    });

    if (!res.ok) {
      console.error("Error HTTP al obtener eventos:", res.status);
      emptyMsg.textContent = "No se pudo obtener la lista de eventos.";
      emptyMsg.style.display = "block";
      return;
    }

    const data = await res.json();
    const events = data.events || data || [];

    if (events.length === 0) {
      emptyMsg.textContent = "No hay eventos registrados.";
      emptyMsg.style.display = "block";
      return;
    }

    for (const ev of events) {
      const tr = document.createElement("tr");

      const score = (ev.score !== null && ev.score !== undefined)
        ? ev.score.toFixed(2)
        : "-";

      const cmdShort = ev.raw_cmd && ev.raw_cmd.length > 60
        ? ev.raw_cmd.slice(0, 60) + "..."
        : (ev.raw_cmd || "");

      tr.innerHTML = `
        <td>${ev.id}</td>
        <td>${ev.timestamp || ""}</td>
        <td>${ev.source_ip || ""}</td>
        <td>${ev.label || ""}</td>
        <td>${score}</td>
        <td><code>${cmdShort}</code></td>
        <td>
          <button class="btn btn-sm btn-outline-danger btn-delete" data-id="${ev.id}">
            Eliminar
          </button>
        </td>
      `;

      tbody.appendChild(tr);
    }

    // Listeners de eliminar
    tbody.querySelectorAll(".btn-delete").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-id");
        if (!confirm(`¿Eliminar evento ${id}?`)) return;

        try {
          const delRes = await fetch(`${API_BASE}/admin/delete-event/${id}`, {
            method: "DELETE",
            headers: {
              "Authorization": `Bearer ${getToken()}`
            }
          });

          if (!delRes.ok) {
            alert("No se pudo eliminar el evento.");
            return;
          }

          // Recargar la tabla
          loadEvents();
        } catch (err) {
          console.error("Error al eliminar evento:", err);
          alert("Error de conexión al eliminar.");
        }
      });
    });

  } catch (err) {
    console.error("Error cargando eventos:", err);
    emptyMsg.textContent = "Error de conexión al obtener eventos.";
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

  const btnRefresh = document.getElementById("btn-refresh");
  if (btnRefresh) {
    btnRefresh.addEventListener("click", () => {
      loadEvents();
    });
  }

  // Cargar eventos al inicio
  loadEvents();
});
