#include <PWM.h>

#define pwmPin1 9
#define inA1 11
#define inB1 4
#define pwmPin2 10
#define inA2 5
#define inB2 6
#define pwmPin3 3
#define inA3 7
#define inB3 8

// #define comDir 12

// PWM pins : 3, 5, 6, 9, 10, 11?
int pwmFrequency = 20000;
const int MAX_BYTES = 6;
// int time = 0;
// int lastTime = 0;
// int count = 0;

// Variables to hold data from serial
uint8_t data[MAX_BYTES];

void setup() {
  InitTimersSafe();
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  pinMode(inA1, OUTPUT);
  pinMode(inB1, OUTPUT);
  pinMode(inA2, OUTPUT);
  pinMode(inB2, OUTPUT);
  pinMode(inA3, OUTPUT);
  pinMode(inB3, OUTPUT);

  // // For bi-directional RS-485
  // pinMode(comDir, OUTPUT);

  // Set PWM pins to output and to the right frequency
  pinMode(pwmPin1, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(pwmPin3, OUTPUT);
  SetPinFrequencySafe(pwmPin1, pwmFrequency);
  SetPinFrequencySafe(pwmPin2, pwmFrequency);
  SetPinFrequencySafe(pwmPin3, pwmFrequency);
}

void loop() {
  int ret = Serial.readBytes(data, MAX_BYTES);
  // time += millis() - lastTime;
  // lastTime = millis();
  // if (time > 1000){
  //   digitalWrite(comDir, HIGH);
  //   delay(10);
  //   Serial.write(count);
  //   count++;
  //   digitalWrite(comDir, LOW);
  //   time = 0;
  // }
  while (Serial.available() > 0) {
    Serial.read();
  }
  if (ret == MAX_BYTES) {
    pwmWrite(pwmPin1, data[1]);
    switch (data[0]) {
    case 1: digitalWrite(inA1, LOW); digitalWrite(inB1, HIGH); break;
    case 0: digitalWrite(inA1, LOW); digitalWrite(inB1, LOW); break;
    case 2: digitalWrite(inA1, HIGH); digitalWrite(inB1, LOW); break;
    }
    pwmWrite(pwmPin2, data[3]);
    switch (data[2]) {
    case 1: digitalWrite(inA2, LOW); digitalWrite(inB2, HIGH); break;
    case 0: digitalWrite(inA2, LOW); digitalWrite(inB2, LOW); break;
    case 2: digitalWrite(inA2, HIGH); digitalWrite(inB2, LOW); break;
    }
    pwmWrite(pwmPin3, data[5]);
    switch (data[4]) {
    case 1: digitalWrite(inA3, LOW); digitalWrite(inB3, HIGH); break;
    case 0: digitalWrite(inA3, LOW); digitalWrite(inB3, LOW); break;
    case 2: digitalWrite(inA3, HIGH); digitalWrite(inB3, LOW); break;
    }
  }
}