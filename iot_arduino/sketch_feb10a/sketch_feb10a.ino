#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <SPI.h>
#include <Wire.h>
#include <Arduino_JSON.h>
#include <ArduinoJson.h>
//#include <Adafruit_GFX.h>
//#include <Adafruit_SSD1306.h>
#include "DHT.h"
#define WIRE Wire
//Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &WIRE);
#define DHTPIN 14     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);
const char* ssid = "phill";
const char* password = "00000000";
int count = 0;
String serverName = "http://172.20.10.3:3000";
int sw_fan = 16;
int lamp = 13;
int fan = 12;
int water = 2;
int sw_water = 1;
int sw_lamp = 3;
unsigned long lastTime = 0;
unsigned long lastTime_get = 0;
unsigned long timerDelay = 5000;
unsigned long timerDelay_get = 1000;
String payload_get_fan = "";
String payload_get_water = "";
String payload_get_lamp = "";
String payload_status = "";
const char* status_obj = "";
void setup() {
  pinMode(A0, INPUT);
  Serial.begin(115200);
  pinMode(sw_fan, INPUT);
  pinMode(sw_water, INPUT);
  pinMode(sw_lamp, INPUT);
  pinMode(lamp, OUTPUT);
  pinMode(fan, OUTPUT);
  pinMode(water,OUTPUT);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  dht.begin();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
//  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}

void loop() {
  int adc = analogRead(A0);
  float humid = dht.readHumidity();
  float temp = dht.readTemperature();
  //  Serial.println(adc);
  WiFiClient client;
  HTTPClient http;
  if ((millis() - lastTime_get) > timerDelay_get) {
    //Check WiFi connection status
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("/get_status");
      String serverPath = serverName + "/get_status";
      http.begin(client, serverPath);
      int httpResponseCode = http.GET();
      payload_status = http.getString();
    }
    lastTime_get = millis();
  }
  if (digitalRead(sw_fan) == 0) {
    Serial.print("if");
    while (digitalRead(sw_fan) != 1);
    Serial.print("while");
    String serverPath = serverName + "/change_state_fan";
    http.begin(client, serverPath);
    int httpResponseCode = http.GET();
    payload_get_fan = http.getString();
    //        Serial.print(payload_get_fan[2]);
  }
  if (digitalRead(sw_water) == 0) {
    while (digitalRead(sw_water) != 1);
    String serverPath = serverName + "/change_state_water";
    http.begin(client, serverPath);
    int httpResponseCode = http.GET();
    payload_get_fan = http.getString();
  }
  if (digitalRead(sw_lamp) == 0) {
    while (digitalRead(sw_lamp) != 1);
    String serverPath = serverName + "/change_state_lamp";
    http.begin(client, serverPath);
    int httpResponseCode = http.GET();
    payload_get_fan = http.getString();
  }

  payload_get_fan = String(payload_status[2]);
  payload_get_lamp = String(payload_status[4]);
  payload_get_water = String(payload_status[6]);
  if (payload_get_fan == "0") {
    digitalWrite(fan, 0);
  } else if (payload_get_fan == "1") {
    digitalWrite(fan, 1);
  }
  if (payload_get_lamp == "0") {
    digitalWrite(lamp, 0);
  } else if (payload_get_lamp == "1") {
    digitalWrite(lamp, 1);
  }
    if (payload_get_water == "0") {
      digitalWrite(water, 0);
    } else if (payload_get_water == "1") {
      digitalWrite(water, 1);
    }
  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    if (WiFi.status() == WL_CONNECTED) {

      String serverPath = serverName + "/hello?temp=" + String(temp, 2) + "&&humid=" + String(humid , 2) + "&&adc=" + String(adc);

      // Your Domain name with URL path or IP address with path
      Serial.print("HTTP Response code: ");
      http.begin(client, serverPath);

      // Send HTTP GET request
      int httpResponseCode = http.GET();
      if (httpResponseCode > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.println(payload);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}
