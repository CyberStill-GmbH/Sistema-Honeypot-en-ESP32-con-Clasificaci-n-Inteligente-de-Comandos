const API_BASE = "http://127.0.0.1:8080/siem/api";

function getToken() {
  return localStorage.getItem("siem_jwt");
}

// Si no hay token → vuelve al login
if (!getToken()) {
  window.location.href = "/login.html";
}

async function loadEvents() {
  try {
    const res = await fetch(`${API_BASE}/events`, {
      headers: {
        "Authorization": `Bearer ${getToken()}`
      }
    });

    if (!res.ok) {
      console.error("Error HTTP en /events:", res.status);
      return;
    }

    const data = await res.json();
    const tbody = document.getElementById("events-tbody");
    tbody.innerHTML = "";

    data.forEach(e => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${e.id}</td>
        <td>${e.source_ip}</td>
        <td>${e.raw_cmd}</td>
        <td class="status-${e.label}">${e.label}</td>
        <td>${e.score.toFixed(2)}</td>
        <td>${e.reason}</td>
        <td>${new Date(e.created_at).toLocaleString()}</td>
      `;

      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Error cargando eventos:", err);
  }
}



async function loadSummary() {
  try {
    const res = await fetch(`${API_BASE}/stats/summary`, {
      headers: {
        // Si en tu backend protegiste /stats con JWT, esto lo usa.
        // Si no está protegido, no pasa nada por enviarlo igual.
        "Authorization": `Bearer ${getToken()}`
      }
    });

    if (!res.ok) {
      console.error("Error HTTP en /stats/summary:", res.status);
      return;
    }

    const data = await res.json();

    // OJO: depende de cómo devuelves los campos en tu API stats
    // Yo asumí: { total_events, by_label, events_today, unique_ips }
    document.getElementById("metric-total").textContent =
      data.total_events ?? 0;

    const byLabel = data.by_label || {};
    const sospechosos =
      byLabel["sospechoso"] ||
      byLabel["suspicious"] ||
      byLabel["SUSPICIOUS"] ||
      0;

    const exploits =
      byLabel["exploit"] ||
      byLabel["EXPLOIT"] ||
      0;

    document.getElementById("metric-suspicious").textContent = sospechosos;
    document.getElementById("metric-exploit").textContent = exploits;
  } catch (err) {
    console.error("Error cargando summary:", err);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // Botón de logout
  const btnLogout = document.getElementById("btn-logout");
  if (btnLogout) {
    btnLogout.addEventListener("click", () => {
      localStorage.removeItem("siem_jwt");
      window.location.href = "/login.html";
    });
  }

  // Cargar métricas
  loadSummary();
  setInterval(loadSummary, 10000);
  loadEvents();
  setInterval(loadEvents, 10000); // refresca cada 10s

});
