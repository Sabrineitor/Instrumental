/*
*/

# include <Time.h>

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

  analogWrite(pinIn,25);

  int valor = 0;
  
  for ( int ii=0; ii < 200 ; ii=ii+1 ) {
   Vread = analogRead(pinRead);
   
   valor = valor + Vread;
   delay(11.3);
   
  }
  
  //Vread = analogRead(pinRead);
  ;
  
  // print out the value you read:
  Serial.println(valor);
  //delay(500);        // delay in between reads for stability
}
