// Pin definitions for entry and exit IR sensors
const int entryIR1 = 5;
const int exitIR1 = 4;


// Variables to store timing information
unsigned long entryStartTime = 0;
unsigned long exitStartTime = 0;

// Flags to check if sensors have been high long enough
bool entryDetected = false;
bool exitDetected = false;

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <NTPClient.h>

const char* ssid     = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";

// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 19800 , 30000); // Update every 60 seconds

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

  // Initialize NTP client
  timeClient.begin();
}

void loop() {

  timeClient.update();
  unsigned long epochTime = timeClient.getEpochTime();
  int currentHour = timeClient.getHours();
  int currentMinute = timeClient.getMinutes();
  int currentSecond = timeClient.getSeconds();

  // Read sensor states
  int entryIR1State = digitalRead(entryIR1);
  int entryIR2State = digitalRead(entryIR2);
  int exitIR1State = digitalRead(exitIR1);
  int exitIR2State = digitalRead(exitIR2);

  // Check entry detection condition
  if (entryIR1State == LOW ) {
    if (entryStartTime == 0) {
      entryStartTime = millis(); // Start timing if sensors are both high
    }
    if (millis() - entryStartTime >= 500 && !entryDetected) {
      Serial.print("Entry detected at :");
      Serial.print(currentHour);
      Serial.print(" hr : ");
      Serial.print(currentMinute);
      Serial.print(" min : ");
      Serial.print(currentSecond);
      Serial.println(" sec");
      entryDetected = true; // Mark as detected to avoid repeated prints
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
    if (millis() - exitStartTime >= 500 && !exitDetected) {
      Serial.print("Exit detected at : ");
      Serial.print(currentHour);
      Serial.print(" hr : ");
      Serial.print(currentMinute);
      Serial.print(" min : ");
      Serial.print(currentSecond);
      Serial.println(" sec");
      exitDetected = true; // Mark as detected to avoid repeated prints
    }
  } else {
    exitStartTime = 0; // Reset timing if sensors go low
    exitDetected = false; // Reset flag to allow new detection
  }
}
