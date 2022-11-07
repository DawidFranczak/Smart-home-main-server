#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_PWMServoDriver.h>

#define WIFILED D4
#define SENSORDOWN D5
#define SENSORUP D6
#define ADDBUTTON D7


// Połączenie z siecą WiFi
const char* ssid = "Tenda";
const char* password = "1RKKHAPIEJ";

// const char* ssid = "UPC917D5E9";
// const char* password = "7jxkHw2efapT";

// Port oraz ip uC
unsigned int udpPort = 2965;
WiFiUDP UDP;

// Odbieranie oraz wysyłani danych
char dataPackage[255];
int paczkaDanych;
String date;

// Ustawienia jasnośći oraz ilości kroków
int brightness = 4096;
int step = 21;
int stairsNumber = 16;

// Czas zapalenia oświetlenia
unsigned long startTime = 0;
unsigned long presentTime = 0;
unsigned long lightingTime = 10000;

// Logika
bool sensorUp = false;
bool sensorDown = false;
bool lightOn = false;
bool on = false;

// Utworzenie obiektu pwm o adresie 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

void off();
void turnOffSensorDown();
void turnOffSensorUp();
void turnOnSensorDown();
void turnOnSensorUp();

void setup() {
  pinMode(WIFILED,OUTPUT);
  pinMode(SENSORDOWN,INPUT_PULLUP);
  pinMode(SENSORUP,INPUT_PULLUP);
  pinMode(ADDBUTTON,INPUT_PULLUP);

  digitalWrite(WIFILED,HIGH);
  WiFi.begin(ssid,password);
  UDP.begin(udpPort);
  pwm.begin();
  pwm.setPWMFreq(500);
  off();
  Serial.begin(9600);
}

void loop() {
  if(WiFi.status() == WL_CONNECTED)   digitalWrite(WIFILED,LOW);
  else digitalWrite(WIFILED,HIGH);
  
  paczkaDanych = UDP.parsePacket();
  if(paczkaDanych){
    int len = UDP.read(dataPackage, 255);
    if (len > 0) dataPackage[len] = 0;
    date = dataPackage;
    Serial.println(date);

    if (date == "password_stairs" && digitalRead(ADDBUTTON) == HIGH) { 
      UDP.beginPacket(UDP.remoteIP(), UDP.remotePort()); 
      UDP.write("respond_stairs");
      UDP.endPacket();
    }
    // else if(date =="ON") {
    //   if(!lightOn) turnOnSensorDown();
    //   on = true;
    // }
    // else if(date =="OFF") {
    //   if(lightOn) turnOffSensorDown();
    //   on = false;
    // }
    else if(date.substring(0,2) == "sp"){
      step = 4096/date.substring(2).toInt(); 
      Serial.print("step ");
      Serial.println(step);
      Serial.println("\n");
      }
    else if(date.substring(0,2) == "bs") {
      brightness = (4096*date.substring(2).toInt())/100;
      Serial.println("brightness ");
      Serial.println(brightness);
      Serial.println("\n");

    }
    else if(date.substring(0,2) == "te") {
      lightingTime = 1000*date.substring(2).toInt();
      Serial.println("lightingTime ");
      Serial.println(lightingTime);
      Serial.println("\n");

    }
  }
  // if(digitalRead(SENSORDOWN) == HIGH){
  //   delay(20);
  //   if(digitalRead(SENSORDOWN) == HIGH && sensorUp == false && sensorDown == false){
  //     if(!lightOn) {
  //       Serial.print("Sensor down");
  //       turnOnSensorDown();
  //       sensorDown = true;
  //       startTime = millis();
  //       }
  //   }
  // }
  // else if(digitalRead(SENSORUP) == HIGH){
  //   delay(20);
  //   if(digitalRead(SENSORUP) == HIGH && sensorUp == false && sensorDown == false){
  //     if(!lightOn) {
  //       Serial.print("Sensor up");
  //       turnOnSensorUp();
  //       sensorUp = true;
  //       startTime = millis();
  //     }
  //   }
  // }

  // Odmierzanie czasu do zgaszenia lamp
  presentTime = millis();
  if(presentTime - startTime >=lightingTime && sensorDown && on == false ){
    turnOffSensorDown();
  }
  if(presentTime - startTime >=lightingTime && sensorUp && on == false ){
    turnOffSensorUp();
  }
}

void off()
{
  for (int i = 0; i < 16; i++)
  {
    pwm.setPin(i,0);
  }
}
void turnOffSensorDown(){
  for(int nr = 0; nr < stairsNumber; nr++){
    for(int i = brightness-1; i > 0; i=i-step){
      pwm.setPin(nr,i);
      delay(1);
      if(i <= step) pwm.setPin(nr,0);
    }
  }
  sensorUp = false;
  lightOn = false;
  sensorDown = false;
  while(digitalRead(SENSORDOWN) == HIGH) delay(1);
}
void turnOffSensorUp(){
    for(int nr = stairsNumber; nr > -1; nr--){
    for(int i = brightness-1; i > 0; i=i-step){
      pwm.setPin(nr,i);
      delay(1);
      if(i <= step)  pwm.setPin(nr,0);
    }
  }
  sensorUp = false;
  lightOn = false;
  sensorDown = false;
  while(digitalRead(SENSORUP) == HIGH) delay(1);
}
void turnOnSensorDown(){ 
  for(int nr = 0; nr < stairsNumber; nr++){
    for(int i = 0; i < brightness-1; i=i+step){
      pwm.setPin(nr,i);
      delay(1);
      if(i+step > brightness) pwm.setPin(nr,brightness);
    }
  }
  lightOn = true;
}
void turnOnSensorUp(){
  for(int nr = stairsNumber; nr > -1; nr--){
    for(int i = 0; i < brightness-1; i=i+step){
      pwm.setPin(nr,i);
      delay(1);
      if (i+step > brightness) pwm.setPin(nr,brightness);
    }
  }
  lightOn = true;
}