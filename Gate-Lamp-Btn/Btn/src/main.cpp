#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define BUTTON 2     // Przycisk do włączenia oświetlenia
#define WIFILED 1    // Sygnalizcja podłączenia do wifi

// Połączenie z siecą WiFi
// const char* ssid = "Tenda";
// const char* password = "1RKKHAPIEJ";

const char* ssid = "UPC917D5E9";
const char* password = "7jxkHw2efapT";

// Porty oraz ip do komunikacji
char serwerIp [15] = "192.168.0.52";
int serwerPort = 6785;

// Port oraz ip uC
unsigned int UdpPort = 7894;
WiFiUDP UDP;

// Odbieranie oraz wysyłani danych
int paczkaDanych;
char dataPackage[255];
String date;


// Ustawienie czasu wciśnięcia przycisku 
unsigned long presenTime;
unsigned long startTime;
unsigned long pressTime = 1000;
bool click = false;


void setup() {
  // Inicjalizacja
  pinMode(BUTTON,INPUT_PULLUP);
  pinMode(WIFILED,OUTPUT);

  // Serial.begin(9600);
  WiFi.begin(ssid,password);
  UDP.begin(UdpPort);
  while (WiFi.status() != WL_CONNECTED) delay(1);
  Serial.print(WiFi.localIP());

}

void loop() {
  // Sygnalizacja podłączenia wifi
  // if(WiFi.status() == WL_CONNECTED)  digitalWrite(WIFILED,LOW);
  // else digitalWrite(WIFILED,HIGH);

  paczkaDanych = UDP.parsePacket();
  if(paczkaDanych){
    int len = UDP.read(dataPackage, 255);
    if (len > 0) dataPackage[len] = 0;
      date = dataPackage;
      
       // Dodanie urządzneia
    if (date == "password_btn") { 
      UDP.beginPacket(UDP.remoteIP(), UDP.remotePort()); 
      UDP.write("respond_btn");
      UDP.endPacket();
    } 
  }

  // Włączenie lamp z przycisku 
  if(digitalRead(BUTTON) == LOW && click == false){
    delay(30);
    if(digitalRead(BUTTON) == LOW){
      startTime = millis();
      click = true;
    }
  }
  presenTime = millis();
  if(presenTime - startTime >= pressTime && click ){
  // Włączenie lamp bez limitu czasowego
    if(digitalRead(BUTTON) == LOW){
      UDP.beginPacket(serwerIp, serwerPort);
      UDP.write("still");
      UDP.endPacket(); 
      while(digitalRead(BUTTON) == LOW) delay(1);
      click = false;
    }
    // Włączenie lamp z limitem czasowym 
    else{
      UDP.beginPacket(serwerIp, serwerPort);
      UDP.write("click");
      UDP.endPacket();
      click = false;
    }
  }
}