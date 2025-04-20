//header files for http requests and wifi acesss
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Pin definitions for entry and exit IR sensors
const int entryIR1 = 5;
const int exitIR1 = 4;

// Variables to store timing information
unsigned long entryStartTime = 0;
unsigned long exitStartTime = 0;

// Flags to check if sensors have been high long enough
bool entryDetected = false;
bool exitDetected = false;

//wifi credential for connecting to network
const char* ssid     = "errr";
const char* password = "err@12345";

const char* serverIP = "http://192.168.166.179:5000";

void setup() {
  // Initialize serial monitor
  Serial.begin(115200);
  
  // Set up pins for the sensors
  pinMode(entryIR1, INPUT);
  pinMode(exitIR1, INPUT);
  
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected.");

}

void loop() {
  // Read sensor states
  int entryIR1State = digitalRead(entryIR1);
  int exitIR1State = digitalRead(exitIR1);

  // Check entry detection condition
  if (entryIR1State == LOW ) {
    if (entryStartTime == 0) {
      entryStartTime = millis(); // Start timing if sensors are both high
    }
    if (millis() - entryStartTime >= 300 && !entryDetected) {
      Serial.println("ENTRY DETECTED");
      entryDetected = true;
      if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        WiFiClient client;
        http.begin(client, String(serverIP) + "/log/entry");
        http.POST("");
        http.end();
      }
    }
  } else {
    entryStartTime = 0; // Reset timing if sensors go low
    entryDetected = false; // Reset flag to allow new detection
  }

  // Check exit detection condition
  if (exitIR1State == LOW ) {
    if (exitStartTime == 0) {
      exitStartTime = millis(); // Start timing if sensors are both high
    }
    if (millis() - exitStartTime >= 300 && !exitDetected) {
      Serial.println("EXIT DETECTED");
      exitDetected = true;
      if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        WiFiClient client;
        http.begin(client, String(serverIP) + "/log/exit");
        http.POST("");
        http.end();
      }
    }
  } else {
    exitStartTime = 0; // Reset timing if sensors go low
    exitDetected = false; // Reset flag to allow new detection
  }
}

//legitCoconut
