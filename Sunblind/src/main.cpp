#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <string.h>

#define WIFILED D4

#define IN1 D5
#define IN2 D6
#define IN3 D7
#define IN4 D8

// const char* ssid = "Tenda";
// const char* password = "1RKKHAPIEJ";

const char* ssid = "UPC917D5E9";
const char* password = "7jxkHw2efapT";

int oldPosition = 2048;
int phase = 0;
int maxMove = 2048;
bool up = false, down = false, save = false;

unsigned int UdpPort = 9846;
char data_package[255];
String date;
WiFiUDP UDP;

void step(bool direction);
int calibration();
void setPosition(int newPosition);
void off();

void setup() {
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  pinMode(WIFILED,OUTPUT);

  Serial.begin(9600);
  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED) delay(1);
  UDP.begin(UdpPort);
}

void loop() {
 if (WiFi.status() == WL_CONNECTED) digitalWrite(WIFILED,LOW);
 else digitalWrite(WIFILED,HIGH);


  int dataSize = UDP.parsePacket();
  if(dataSize){
    int len = UDP.read(data_package, 255);
    if (len > 0) data_package[len] = 0;
    date = data_package;
    // Serial.print(date);

    if(date == "password_sunblind"){
      UDP.beginPacket(UDP.remoteIP(), UDP.remotePort()); // odesłanie do nadawcy
      UDP.write("respond_sunblind");
      UDP.endPacket(); 
    }
    else if(date.substring(0,3) == "set"){
      int position = (maxMove * date.substring(3).toInt())/100;
      setPosition(position);
    }
    else if(date == "calibration"){
      maxMove = calibration();
      oldPosition = maxMove;
    }
  }
}

int calibration(){
  int steps = 0;
  while(true){
    int dataSize = UDP.parsePacket();
    if(dataSize){
      int len = UDP.read(data_package, 255);
      if (len > 0) data_package[len] = 0;
      date = data_package;
      if(date == "up"){
        up = true; 
        down = false;
      }
      else if(date == "down"){
        up = false; 
        down = true;
      }
      else if(date == "stop"){
        up = false; 
        down = false;
      }
      else if(date == "save"){
        steps = 0;
      }
      else if(date == "end"){
        return steps;
      }
    }

    if(up){
      step(true);
      steps--;
    }
    else if(down){
      step(false);
      steps++;
    }
  }
  off();
}

void step(bool direction){
  if(direction){
    switch (phase){
      case 0:
        digitalWrite(IN1,HIGH);
        digitalWrite(IN2,LOW);
        digitalWrite(IN3,LOW);
        digitalWrite(IN4,LOW);
        break;
      case 1:
        digitalWrite(IN1,LOW);
        digitalWrite(IN2,HIGH);
        digitalWrite(IN3,LOW);
        digitalWrite(IN4,LOW);
        break;
      case 2:
        digitalWrite(IN1,LOW);
        digitalWrite(IN2,LOW);
        digitalWrite(IN3,HIGH);
        digitalWrite(IN4,LOW);
        break;
      case 3:
        digitalWrite(IN1,LOW);
        digitalWrite(IN2,LOW);
        digitalWrite(IN3,LOW);
        digitalWrite(IN4,HIGH);
        break;
    }
  }
  else{
    switch(phase){
      case 0:
        digitalWrite(IN1,LOW);
        digitalWrite(IN2,LOW);
        digitalWrite(IN3,LOW);
        digitalWrite(IN4,HIGH);
        break;
      case 1:
        digitalWrite(IN1,LOW);
        digitalWrite(IN2,LOW);
        digitalWrite(IN3,HIGH);
        digitalWrite(IN4,LOW);
        break;
      case 2:
        digitalWrite(IN1,LOW);
        digitalWrite(IN2,HIGH);
        digitalWrite(IN3,LOW);
        digitalWrite(IN4,LOW);
        break;
      case 3:
        digitalWrite(IN1,HIGH);
        digitalWrite(IN2,LOW);
        digitalWrite(IN3,LOW);
        digitalWrite(IN4,LOW);
        break;
    }
  }
  delay(3);
  phase++;
  if(phase >4) phase = 0;
  else if (phase<0) phase = 4;
}

void setPosition(int position){
  while(oldPosition != position){
    if(oldPosition > position) {
      step(false);
      oldPosition--;
    }
    else if(oldPosition < position){
      step(true);
      oldPosition++;
    }
  }
  off();
}

void off(){
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,LOW);
}