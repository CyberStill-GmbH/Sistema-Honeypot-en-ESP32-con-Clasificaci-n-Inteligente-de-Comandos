# Proyecto 1 — ESP32 + IA que Detecta Comandos Sospechosos

## Objetivo
Backend Python que recibe comandos desde un ESP32, los clasifica en tiempo real usando IA (o reglas fallback),
genera alertas y guarda eventos en CSV. Incluye ejemplo de sketch para ESP32 que envía comandos por UDP.

## Estructura
```
esp32_ia_backend/
├─ clasificador.py
├─ server_wifi_udp.py
├─ server_wifi_flask.py
├─ logger_csv.py
├─ utils.py
├─ train_model.py
├─ requirements.txt
├─ README.md
├─ esp32_udp_example.ino
├─ .gitignore
└─ tests/
   └─ test_clasificador.py
```

## Quickstart (local)
1. Crear y activar virtualenv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # mac/linux
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar servidor UDP:
   ```bash
   python server_wifi_udp.py --host 0.0.0.0 --port 9999
   ```
4. Probar con netcat (simula ESP32):
   ```bash
   echo "get temp" | nc -u -w1 127.0.0.1 9999
   ```
5. Ver `events.csv` para revisar logs.

## ESP32
El archivo `esp32_udp_example.ino` es un sketch mínimo que envía strings por UDP al backend y recibe ACK.

## Entrenamiento de modelo (opcional)
`train_model.py` contiene un script simple para entrenar un clasificador de texto (sintético) y guardar `models/modelo_persona2.joblib`.
Puedes usarlo como plantilla para entrenar con tus datos reales.

## Seguridad y Producción (recomendaciones)
- Añadir autenticación (HMAC con clave compartida) para validar mensajes del ESP32.
- Usar HTTPS / TLS si usas WebSocket/HTTP.
- Rotación de logs, size limit y backup.
- Control de acceso a la red (firewall) y whitelisting de IPs del ESP32.
