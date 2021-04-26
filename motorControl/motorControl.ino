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

// PWM pins : 3, 5, 6, 9, 10, 11?
int pwmFrequency = 20000;

// Variables to hold data from serial
int data[6];

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

  // Set PWM pins to output and to the right frequency
  pinMode(pwmPin1, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(pwmPin3, OUTPUT);
  SetPinFrequencySafe(pwmPin1, pwmFrequency);
  SetPinFrequencySafe(pwmPin2, pwmFrequency);
  SetPinFrequencySafe(pwmPin3, pwmFrequency);
}

void loop() {
  if (Serial.available() >= 6) {
    digitalWrite(LED_BUILTIN, HIGH);
    for (int i = 0; i < 6; i ++) {
      data[i] = Serial.read();
    }
    pwmWrite(pwmPin1, data[1]);
    switch (data[0]) {
    case 0: digitalWrite(inA1, LOW); digitalWrite(inB1, HIGH); break;
    case 1: digitalWrite(inA1, LOW); digitalWrite(inB1, LOW); break;
    case 2: digitalWrite(inA1, HIGH); digitalWrite(inB1, LOW); break;
    }
    pwmWrite(pwmPin2, data[3]);
    switch (data[2]) {
    case 0: digitalWrite(inA2, LOW); digitalWrite(inB2, HIGH); break;
    case 1: digitalWrite(inA2, LOW); digitalWrite(inB2, LOW); break;
    case 2: digitalWrite(inA2, HIGH); digitalWrite(inB2, LOW); break;
    }
    pwmWrite(pwmPin3, data[5]);
    switch (data[4]) {
    case 0: digitalWrite(inA3, LOW); digitalWrite(inB3, HIGH); break;
    case 1: digitalWrite(inA3, LOW); digitalWrite(inB3, LOW); break;
    case 2: digitalWrite(inA3, HIGH); digitalWrite(inB3, LOW); break;
    }
  }
}