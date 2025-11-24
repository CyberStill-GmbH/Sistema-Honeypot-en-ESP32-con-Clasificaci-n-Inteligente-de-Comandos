#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <WiFiUdp.h>
#include "config.h"  // Incluir las credenciales de WiFi desde config.h

#define WIFI_CHANNEL 6

WebServer server(80);
WiFiUDP udp;

const int LED1 = 26;
const int LED2 = 27;

bool led1State = false;
bool led2State = false;

// Dirección IP del PC que recibirá los comandos
IPAddress pcIPAddress(192, 168, 18, 21);  // Ajusta a la IP del PC que recibirá los comandos

// ------------------- Conexión WiFi -------------------
void conectarWiFi() {
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado");
  Serial.print("IP del ESP32: ");
  Serial.println(WiFi.localIP());
}

// ------------------- Reenvío del comando -------------------
void reenviarComando(const String& cmd) {
  // Log local
  Serial.print("[HONEY] Comando recibido: ");
  Serial.println(cmd);

  // Enviar el comando por UDP al PC
  udp.beginPacket(pcIPAddress, 6060);  // Puerto 6060 para el servidor
  udp.print(cmd);
  udp.endPacket();
}

// ------------------- Handler HTTP /cmd -------------------
void handleCmd() {
  if (!server.hasArg("cmd")) {
    server.send(400, "text/plain", "Falta parametro cmd");
    return;
  }

  String cmd = server.arg("cmd");

  // Log y reenvío del comando por UDP al PC
  reenviarComando(cmd);

  // Responder con OK al atacante
  server.send(200, "text/plain", "Comando recibido: " + cmd);
}

// ------------------- Configuración de servidor HTTP -------------------
void configurarServidorHTTP() {
  server.on("/", HTTP_GET, []() {
    String response = R"(
      <!DOCTYPE html><html>
        <head>
          <title>ESP32 Honeypot IoT</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            html { font-family: sans-serif; text-align: center; }
            body { display: inline-flex; flex-direction: column; }
            h1 { margin-bottom: 1.2em; } 
            h2 { margin: 0; }
            .btn { background-color: #5B5; border: none; color: #fff; padding: 0.5em 1em;
                   font-size: 2em; text-decoration: none }
            .btn.OFF { background-color: #333; }
          </style>
        </head>
        <body>
          <h1>ESP32 Honeypot IoT</h1>
          <h2>Comandos disponibles</h2>
          <p><a href="/cmd?cmd=LED_ON" class="btn">Encender LED</a></p>
          <p><a href="/cmd?cmd=LED_OFF" class="btn OFF">Apagar LED</a></p>
          <p><a href="/cmd?cmd=ATTACK" class="btn OFF">Simular ataque</a></p>
        </body>
      </html>
    )";
    server.send(200, "text/html", response);
  });

  server.on("/cmd", HTTP_GET, handleCmd);  // Manejo de comandos por GET

  server.begin();
  Serial.println("Servidor HTTP iniciado en puerto 80");
}

// ------------------- Setup -------------------
void setup(void) {
  Serial.begin(115200);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  conectarWiFi();

  // Iniciar UDP en el puerto 6060 para enviar comandos al PC
  udp.begin(6060);

  configurarServidorHTTP();  // Configuración del servidor HTTP
}

// ------------------- Loop -------------------
void loop(void) {
  server.handleClient();  // Manejar las peticiones HTTP
  delay(2);
}
