#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <string.h>
#include <DHT.h>
#include <Adafruit_Sensor.h>

#define ADDBUTTON 0
#define DHTPIN 2
#define DHTTYPE DHT11 

// const char* ssid = "Tenda";
// const char* password = "1RKKHAPIEJ";


const char* ssid = "UPC917D5E9";
const char* password = "7jxkHw2efapT";

unsigned int UdpPort = 1265;
char data_package[255];
char rep_buffer[10];
int paczkaDanych;
String date;
WiFiUDP UDP;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(ADDBUTTON,INPUT_PULLUP);
  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED) delay(1);
  UDP.begin(UdpPort);
  dht.begin();
}

void loop() {
  while(true){
    paczkaDanych = UDP.parsePacket();
    if(paczkaDanych){
      int len = UDP.read(data_package, 255);
      if (len > 0)
      {
        data_package[len] = 0;
      }
      date = data_package;
      if(digitalRead(ADDBUTTON)==LOW){
        delay(20);
        if(date == "password_temp" && digitalRead(ADDBUTTON)==LOW){
          UDP.beginPacket(UDP.remoteIP(), UDP.remotePort()); // odesłanie do nadawcy
          UDP.write("respond_temp");
          UDP.endPacket(); 
          delay(200);
        }
      }
      else if(date == "pomiar"){
        float h = dht.readHumidity();
        float t = dht.readTemperature();
        dtostrf(t, 2, 2, rep_buffer);
        UDP.beginPacket(UDP.remoteIP(), UDP.remotePort()); // odesłanie do nadawcy
        UDP.write(rep_buffer);
        UDP.endPacket(); 
        delay(200);
        break;
      }
    }
  }
  // ESP.deepSleep(10E6);
}