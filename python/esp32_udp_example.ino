// Ejemplo mínimo ESP32 — enviar comandos por UDP y recibir ACK
#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "TU_SSID";
const char* password = "TU_PASSWORD";
const char* host = "192.168.1.100"; // IP del servidor donde corre el backend
const int port = 9999;

WiFiUDP udp;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Conectando WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" conectado");
  udp.begin(WiFi.localIP(), port+1);
}

void loop() {
  // comando ejemplo — cambia o lee desde Serial
  String cmd = "get temp";
  udp.beginPacket(host, port);
  udp.write(cmd.c_str());
  udp.endPacket();

  // esperar respuesta (ACK)
  int size = udp.parsePacket();
  unsigned long start = millis();
  while (millis() - start < 1000) {
    int len = udp.parsePacket();
    if (len) {
      char buf[256];
      int r = udp.read(buf, 255);
      if (r > 0) buf[r] = 0;
      Serial.print("ACK recibido: ");
      Serial.println(buf);
      break;
    }
    delay(10);
  }

  delay(5000);
}
