void setup() {
  pinMode(5, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  delay(1000);
  digitalWrite(5, HIGH);
  digitalWrite(2, HIGH);
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(5, LOW);
  digitalWrite(2, LOW);
  digitalWrite(13, LOW);
}