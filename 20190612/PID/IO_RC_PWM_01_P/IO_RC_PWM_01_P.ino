/*
*/
int pinIn = 11;
int pinRead = A0;
int Vin = 0;  // Vin = (0, 255)
int Vread = 4000;
int error;  // variable error
double P = 0.2 ;  // variable proporcional
int setpoint = 50;

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(pinIn, OUTPUT); // sets the pin as output
}

// the loop routine runs over and over again forever:
void loop() {

  analogWrite(pinIn,Vin);  
  Vread = analogRead(pinRead);
  error = setpoint - Vread;
  Vin = P*error;
  
  // print out the value you read:
  Serial.println(Vread);
  delay(100);        // delay in between reads for stability
}
