#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <string.h>

#define LIGHT 0
#define WIFILED 1
#define ADDBUTTON 2


const char* ssid     = "Tenda";
const char* password = "1RKKHAPIEJ";

// const char* ssid = "UPC917D5E9";
// const char* password = "7jxkHw2efapT";

unsigned int UdpPort = 4324;
char data_package[255];
int paczkaDanych;
String date;
WiFiUDP UDP;

void setup() {
  Serial.begin(9600);
  pinMode(LIGHT,OUTPUT);
  pinMode(WIFILED,OUTPUT);
  pinMode(ADDBUTTON,INPUT_PULLUP);

  digitalWrite(LIGHT,HIGH);
  digitalWrite(WIFILED,HIGH);
  UDP.begin(UdpPort);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(1); 

}

void loop() {
  if (WiFi.status() == WL_CONNECTED) digitalWrite(WIFILED,LOW);
  else digitalWrite(WIFILED,HIGH);
  paczkaDanych = UDP.parsePacket();
  if(paczkaDanych){
    int len = UDP.read(data_package, 255);
    if (len > 0)
    {
      data_package[len] = 0;
    }
    date = data_package;
    Serial.print(date);
    if(date == "password_light" && digitalRead(ADDBUTTON) == HIGH){   
      UDP.beginPacket(UDP.remoteIP(), UDP.remotePort()); // odesłanie do nadawcy
      UDP.write("respond_light");
      UDP.endPacket(); 
    }
    // }
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