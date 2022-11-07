#include <ESP8266WiFi.h>
#include <Wire.h>
#include <String.h>
#include <WiFiUdp.h>


// Przypisanie pinów
#define SWIETLOWKA D3 
#define WIFILED D4
#define BLUEPIN  D5 
#define GREENPIN  D6 
#define REDPIN D7   
#define ADDBUTTON D8 


// Dane do sieci wifi
const char* ssid     = "Tenda";
const char* password = "1RKKHAPIEJ";

// const char* ssid = "UPC917D5E9";
// const char* password = "7jxkHw2efapT";

unsigned int UdpPort = 7863;
char data_package[255];
String date;

int paczka_danych;

int blue = 255, red = 255, green =255;

bool mode = false;

WiFiUDP UDP;

void setup() {
  UDP.begin(UdpPort);
  Serial.begin(9600);
  pinMode(D4,OUTPUT);
  digitalWrite(D4,HIGH);

  // Konfiguracja pwm
  analogWriteRange(255);
  analogWriteFreq(1000);
  analogWrite(REDPIN, 0);
  analogWrite(GREENPIN, 0);
  analogWrite(BLUEPIN, 0);

  
  //konfiguracja pinów
  pinMode(SWIETLOWKA,OUTPUT); // swietlowka
  pinMode(ADDBUTTON,INPUT_PULLUP);
  //Łączenie z wifi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)  delay(1);
}

void loop(){
  if (WiFi.status() == WL_CONNECTED) digitalWrite(D4,LOW);
  else digitalWrite(D4,HIGH);

  paczka_danych = UDP.parsePacket();
  if(paczka_danych){
    int len = UDP.read(data_package, 255);
    if (len > 0) data_package[len] = 0;

    date = data_package;
    Serial.println(date);
    Serial.println(digitalRead(ADDBUTTON));

    if (date == "r1"){
      analogWrite(BLUEPIN, blue);
      analogWrite(GREENPIN, green);
      analogWrite(REDPIN, red);
      mode = true;
    }
    else if (date == "r0"){
      analogWrite(BLUEPIN,0);
      analogWrite(GREENPIN, 0);
      analogWrite(REDPIN, 0);
      mode = false;
    }
    else if(date.substring(0,1) == "r" && mode){
      blue = date.substring(1,date.indexOf("g")).toInt();
      green = date.substring(date.indexOf("g")+1,date.indexOf("b")).toInt();
      red = date.substring(date.indexOf("b")+1).toInt();
      analogWrite(BLUEPIN, blue);
      analogWrite(GREENPIN, green);
      analogWrite(REDPIN, red);
    }
    else if (date == "s0"){
      digitalWrite(SWIETLOWKA,HIGH);
    }
    else if (date == "s1"){
      digitalWrite(SWIETLOWKA,LOW);
    }
    else if (date == "password_aqua" && digitalRead(ADDBUTTON)==HIGH){
        UDP.beginPacket(UDP.remoteIP(), UDP.remotePort()); // odesłanie do nadawcy
        UDP.write("respond_aqua");
        UDP.endPacket();
    }
  }
}