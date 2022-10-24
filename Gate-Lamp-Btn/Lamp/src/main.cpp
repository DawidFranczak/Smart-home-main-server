#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_PWMServoDriver.h>
#include <Wire.h>

#define WIFILED 1 // Sygnalizcja podłączenia do wifi

// Połączenie z siecą WiFi
// const char* ssid = "Tenda";
// const char* password = "1RKKHAPIEJ";

const char* ssid = "UPC917D5E9";
const char* password = "7jxkHw2efapT";

// Czas zapalenia oświetlenia
unsigned long startTime = 0;
unsigned long presentTime = 0;
unsigned long lightingTime = 3000;

// Port oraz ip uC
unsigned int udpPort = 4569;
WiFiUDP UDP;

// Odbieranie oraz wysyłani danych
char dataPackage[255];
int paczkaDanych;
String date;

// Logika
bool lightOnRFID = false;
bool lightOnSwitch = false;
bool lightOn = false;

// Ustawienia jasnośći oraz ilości kroków
int brightness = 4096;
int step = 21;

// Utworzenie obiektu pwm o adresie 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

void off();               // Zgaszenie wszytskich lamp
void turnOnFromRFID();    // Zapalenie poprzez czytkin rfid
void turnOnFromSwitch();  // Zapalenie poprzez przycisk 
void turnOffFromSwitch(); // Zgaszenie świateł zapalonych poprzez przycisk
void turnOffFromRFID();   // Zgaszenie świateł zapalonych poprzez czytnik rfid

void setup() {
  // Inicjalizacja
  pinMode(WIFILED,OUTPUT);
  // Serial.begin(9600);
  Wire.begin(2,0); // Ustawienie magistarli i2c na gpio 2 oraz 0
  WiFi.begin(ssid,password);
  UDP.begin(udpPort);
  pwm.begin();
  pwm.setPWMFreq(500);
  off();
}

void loop() {
  // Sygnalizacja podłączenia wifi
  if(WiFi.status() == WL_CONNECTED)   digitalWrite(WIFILED,LOW);
  else digitalWrite(WIFILED,HIGH);

  // Serial.print(WiFi.localIP());
  // Zaświecenie lamp
  paczkaDanych = UDP.parsePacket();
  if(paczkaDanych){
    int len = UDP.read(dataPackage, 255);
    if (len > 0) dataPackage[len] = 0;
    date = dataPackage;
    // Serial.println("\n");
    // Serial.println(date);
    if (date == "password_lamp") { 
      UDP.beginPacket(UDP.remoteIP(), UDP.remotePort()); 
      UDP.write("respond_lamp");
      UDP.endPacket();
    }
    else if(date == "RFID" ){
      if (lightOnSwitch== false && lightOn == false && lightOnRFID == false){
        turnOnFromRFID();
        lightOnRFID = true;
        startTime = millis();
      }
      else if (lightOnRFID) startTime = millis();
    }
    else if(date == "click"){
      if (lightOnRFID== false && lightOn == false && lightOnSwitch == false){
        turnOnFromSwitch();
        lightOnSwitch = true;
        startTime = millis();
      }
      else if (lightOnSwitch) startTime = millis();
    }
    else if(date == "still" ){
      if (lightOnSwitch == false && lightOnRFID == false && lightOn == false){
        turnOnFromSwitch();
        lightOn = true;
      }
      else if (lightOn){
      turnOffFromSwitch();
      lightOn = false;
      }
    }
    else if(date.substring(0,2) == "bs") brightness = 4096*date.substring(2).toInt()/100;
    else if(date.substring(0,2) == "sp") step = 4096/date.substring(2).toInt(); 
    else if(date.substring(0,2) == "te") lightingTime = 1000*date.substring(2).toInt();
  }
  // Odmierzanie czasu do zgaszenia lamp
  presentTime = millis();
  if(presentTime - startTime >=lightingTime && lightOnRFID){
    turnOffFromRFID();
  }
  if(presentTime - startTime >=lightingTime && lightOnSwitch){
    turnOffFromSwitch();
  }
}

void turnOnFromRFID(){
  for(int nr = 8; nr > -1; nr--){
    for(int i = 0; i < brightness-1; i=i+step){
      pwm.setPin(nr,i);
      delay(1);
      if (i+step > 4095) pwm.setPin(nr,4095);
    }
  }
}
void turnOnFromSwitch(){
  for(int nr = 0; nr < 8; nr++){
    for(int i = 0; i < brightness-1; i=i+step){
      pwm.setPin(nr,i);
      delay(1);
      if(i+step > 4095) pwm.setPin(nr,4095);
    }
  }
}
void turnOffFromSwitch(){
  for(int nr = 0; nr < 8; nr++){
    for(int i = brightness-1; i > 0; i=i-step){
      pwm.setPin(nr,i);
      delay(1);
      if(i <= step) pwm.setPin(nr,0);
    }
  }
  lightOnSwitch = false;
  lightOn = false;
  lightOnRFID = false;
}
void turnOffFromRFID(){
  for(int nr = 8; nr > -1; nr--){
    for(int i = brightness-1; i > 0; i=i-step){
      pwm.setPin(nr,i);
      delay(1);
      if(i <= step)  pwm.setPin(nr,0);
    }
  }
  lightOnSwitch = false;
  lightOn = false;
  lightOnRFID = false;
}
void off()
{
  for (int i = 0; i < 16; i++)
  {
    pwm.setPin(i,0);
  }
}