#include <PWM.h>
#include <OneWire.h> 
#include <DallasTemperature.h>

#define pwmPin1 10 // Left
#define inA1 5
#define inB1 6
#define pwmPin2 9 // Right
#define inA2 11
#define inB 4
#define pwmPin3 3 // UpDown
#define inA3 7
#define inB3 8

#define comDir 12
#define indSwitch 13
#define lightSwitch A5
#define ONE_WIRE_BUS 2

#define voltPin A0

// PWM pins : 3, 5, 6, 9, 10, 11?
int pwmFrequency = 20000;
const int MAX_BYTES = 10;
const int MSG_LEN = 6;
const int NUM_MSG = 5;
int time = 0;
int lastTime = 0;
bool flashing = false;
uint8_t count = 0;
const float R1 = 9.96;
const float R2 = 4.66;

// For temperature sensor
OneWire oneWire(ONE_WIRE_BUS); 
DallasTemperature sensors(&oneWire);

// Variables to hold data from serial
typedef struct data_t_{
  uint8_t req;
  uint8_t m1s;
  uint8_t m2s;
  uint8_t m3s;
  uint8_t m1;
  uint8_t m2;
  uint8_t m3;
  uint8_t state;
} data_t;
uint8_t rawData[MAX_BYTES];
uint8_t msg[NUM_MSG];
data_t data; 

void setup() {
  InitTimersSafe();
  Serial.begin(115200);
  Serial.setTimeout(10);
  pinMode(indSwitch, OUTPUT);
  pinMode(lightSwitch, OUTPUT);
  digitalWrite(lightSwitch, HIGH);
  digitalWrite(indSwitch, LOW);

  pinMode(inA1, OUTPUT);
  pinMode(inB1, OUTPUT);
  pinMode(inA2, OUTPUT);
  pinMode(inB2, OUTPUT);
  pinMode(inA3, OUTPUT);
  pinMode(inB3, OUTPUT);

  // // For bi-directional RS-485
  pinMode(comDir, OUTPUT);

  pinMode(voltPin, INPUT);

  // Set PWM pins to output and to the right frequency
  pinMode(pwmPin1, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(pwmPin3, OUTPUT);
  SetPinFrequencySafe(pwmPin1, pwmFrequency);
  SetPinFrequencySafe(pwmPin2, pwmFrequency);
  SetPinFrequencySafe(pwmPin3, pwmFrequency);

  // Setup temperature sensor on onewire
  sensors.begin();
  sensors.setWaitForConversion(false);

  while (Serial.available() > 0) {
    Serial.read();
  }
}

bool searchMsg(int msgLen) {
  uint8_t ctrl = 0;
  bool found = false;
  for (int i = 0; i <= msgLen-MSG_LEN; i++) {
    if (rawData[i] == 0xAF && rawData[i+1] == 0x55) {
      ctrl = rawData[i+2];
      data.m1 = rawData[i+3];
      data.m2 = rawData[i+4];
      data.m3 = rawData[i+5];
      found = true;
      break;
    }
  }

  if (found) {
    data.m1s = ctrl & 0x3;
    ctrl = ctrl >> 0x2;
    data.m2s = ctrl & 0x3;
    ctrl = ctrl >> 0x2;
    data.m3s = ctrl & 0x3;
    ctrl = ctrl >> 0x2;
    data.req = ctrl & 0x1;
    ctrl = ctrl >> 0x1;
    data.state = ctrl;
  }
  return found;
}

void loop() {
  sensors.requestTemperatures();

  time += millis() - lastTime;
  lastTime = millis();
  if (time > 500 && flashing) {flashing = false; time = 0;}
  if (time > 500 && !flashing) {flashing = true; time = 0;}
  if (data.state == false) {time = 0;}

  for (int i = 0; i < MAX_BYTES; i++) {
    rawData[i] = 0;
  }
  int ret = Serial.readBytes(rawData, MAX_BYTES);
  while (Serial.available() > 0) {
    Serial.read();
  }
  if (searchMsg(ret)) {
    if (data.req == 1) {
      digitalWrite(comDir, HIGH);
      float temperature = sensors.getTempCByIndex(0);
      memcpy(&msg[0], (uint8_t*)&temperature, 4);
      msg[4] = (uint8_t)((((float)analogRead(voltPin))/1024*5*(R1+R2)/R2+0.761)*10);
      Serial.write(msg, NUM_MSG);
      delay(1);
      digitalWrite(comDir, LOW);
    }
    pwmWrite(pwmPin1, data.m1);
    switch (data.m1s) {
      case 1: digitalWrite(inA1, LOW); digitalWrite(inB1, HIGH); break;
      case 2: digitalWrite(inA1, HIGH); digitalWrite(inB1, LOW); break;
      default: digitalWrite(inA1, LOW); digitalWrite(inB1, LOW); break;
    }
    pwmWrite(pwmPin2, data.m2);
    switch (data.m2s) {
      case 1: digitalWrite(inA2, LOW); digitalWrite(inB2, HIGH); break;
      case 2: digitalWrite(inA2, HIGH); digitalWrite(inB2, LOW); break;
      default: digitalWrite(inA2, LOW); digitalWrite(inB2, LOW); break;
    }
    pwmWrite(pwmPin3, data.m3);
    switch (data.m3s) {
      case 1: digitalWrite(inA3, LOW); digitalWrite(inB3, HIGH); break;
      case 2: digitalWrite(inA3, HIGH); digitalWrite(inB3, LOW); break;
      default: digitalWrite(inA3, LOW); digitalWrite(inB3, LOW); break;
    }
  }
  if (data.state && flashing) {
    digitalWrite(indSwitch, HIGH);
  } else {
    digitalWrite(indSwitch, LOW);
  }
  delay(10);
}