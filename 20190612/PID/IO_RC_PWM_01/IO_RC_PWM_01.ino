/*
*/

int pinIn = 11;
int pinRead = A0;
int Vin = 0;
int Vread = 0;

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(pinIn, OUTPUT); // sets the pin as output
}

// the loop routine runs over and over again forever:
void loop() {

  analogWrite(pinIn,127);

  int valor = 0;
  Vread = analogRead(pinRead);
  // print out the value you read:
  Serial.println(Vread);
  delay(100);        // delay in between reads for stability
}
