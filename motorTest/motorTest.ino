#include <PWM.h>

#define analogPin A0
#define analogPinX A1
#define analogPinY A2
#define joyStickBtn 2
#define switch 12

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

// Define variables to hold potentiometre values
int val = 0;
int lastVal = 0;
int valX = 0;
int lastValX = 0;
int valY = 0;
int lastValY = 0;

// Inital values for joystick
int initX = 0;
int initY = 0;
int btn = 0;
int btnD = 0;
int btnL = 0;

// State
int state = 0;
int lastSwitch = 0;

void setup() {
  InitTimersSafe();
  Serial.begin(115200);
  pinMode(joyStickBtn, INPUT_PULLUP);
  pinMode(inA1, OUTPUT);
  pinMode(inB1, OUTPUT);

  // Set PWM pins to output and to the right frequency
  pinMode(pwmPin1, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(pwmPin3, OUTPUT);
  SetPinFrequencySafe(pwmPin1, pwmFrequency);
  SetPinFrequencySafe(pwmPin2, pwmFrequency);
  SetPinFrequencySafe(pwmPin3, pwmFrequency);

  // Init starting positions to joystick
  initX = analogRead(analogPinX);
  initY = analogRead(analogPinY);
}

void loop() {
  // Get values from potentiometres
  val = analogRead(analogPin);
  valX = analogRead(analogPinX) - initX;
  valY = analogRead(analogPinY) - initY;
  btn = digitalRead(joyStickBtn);

  // Stop Joystick from changed too often
  if (valX > -5 and valX < 5) {valX = 0;}
  if (valY > -5 and valY < 5) {valY = 0;}

  if (btn == 0 and btnL == 1) {btnD = 1;}

  if (digitalRead(switch) == 1) {
    state = 0; 
    pwmWrite(pwmPin1, 0);
    digitalWrite(inA1, LOW);
    digitalWrite(inB1, LOW);
    lastSwitch = 1;
  } else if (lastSwitch == 1) {
    state = 1; 
    lastSwitch = 0;
  }

  if (state != 0) {
    if (btnD == 1 and state == 1) {state = 2;}
    else if (btnD == 1 and state == 2) {state = 1;}


    // Write pwm, inA, inB to motor driver
    // if (valY/abs(valY) == 1) {digitalWrite(inA1, HIGH); digitalWrite(inB1, LOW);}
    // if (valY/abs(valY) == -1) {digitalWrite(inA1, LOW); digitalWrite(inB1, HIGH);}
    if (state == 1) {digitalWrite(inA1, HIGH); digitalWrite(inB1, LOW);}
    else if (state == 2) {digitalWrite(inA1, LOW); digitalWrite(inB1, HIGH);}
    pwmWrite(pwmPin1, map(abs(val), 0, 1023, 0, 255));
    pwmWrite(pwmPin2, map(abs(val), 0, 1023, 0, 255));
    pwmWrite(pwmPin3, map(abs(val), 0, 1023, 0, 255));
  }

  // Display values
  Serial.print("Pot: "); Serial.print(val);
  Serial.print(" X: "); Serial.print(valX);
  Serial.print(" Y: "); Serial.print(valY);
  Serial.print(" S: "); Serial.println(state);

  // Delay each loop
  delay(80);

  // Update Last values
  lastVal = val;
  lastValX = valX;
  lastValY = valY;
  btnD = 0;
  btnL = btn;
}