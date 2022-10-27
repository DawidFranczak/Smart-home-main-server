#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <string.h>

#define LIGHT 0
#define ADDBUTTON 2


// const char* ssid = "Tenda";
// const char* password = "1RKKHAPIEJ";

const char* ssid = "UPC917D5E9";
const char* password = "7jxkHw2efapT";

unsigned int UdpPort = 4324;
char data_package[255];
int paczkaDanych;
String date;
WiFiUDP UDP;

void setup() {
  // Serial.begin(9600);
  pinMode(LIGHT,OUTPUT);
  pinMode(ADDBUTTON,INPUT_PULLUP);

  digitalWrite(LIGHT,HIGH);
  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED){ delay(1);  Serial.print(WiFi.localIP());}
  UDP.begin(UdpPort);
}

void loop() {
  paczkaDanych = UDP.parsePacket();
  if(paczkaDanych){
    int len = UDP.read(data_package, 255);
    if (len > 0)
    {
      data_package[len] = 0;
    }
    // date = data_package;
    // Serial.print(date);
     if (digitalRead(ADDBUTTON) == LOW){
      delay(20);
      if(date == "password_light" && digitalRead(ADDBUTTON) == LOW){
        UDP.beginPacket(UDP.remoteIP(), UDP.remotePort()); // odesłanie do nadawcy
        UDP.write("respond_light");
        UDP.endPacket(); 
      }
    }
    else if(date == "change"){
      digitalWrite(LIGHT,!digitalRead(LIGHT));
      UDP.beginPacket(UDP.remoteIP(), UDP.remotePort()); // odesłanie do nadawcy
      if(digitalRead(LIGHT) == LOW){
        UDP.write("ON");
        Serial.print("ON");
      }
      else{
        UDP.write("OFF");
        Serial.print("OFF");
      }
      UDP.endPacket(); 
    }
  }
}