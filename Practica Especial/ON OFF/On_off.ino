#include <Servo.h>

Servo servo1;
int Delta = 20;
int tent6000pin = A0;
int IntensidadActual;
int IntensidadPrevia;



void setup() {
Serial.begin(9600);
 servo1.attach(9);
 servo1.write(15); //Ángulo inicial (5 menos que delta)
 delay(2000);  
}


//si va a cero que se settea a 90


void loop() {

  IntensidadPrevia = analogRead(tent6000pin); //Medí la intensidad (Previa)
  delay(500);                                         

  servo1.write(Delta+1); //Movete a Delta
  delay(500); 
  
  IntensidadActual = analogRead(tent6000pin); //Medí la intensidad (Actual)
  delay(500);  
 
              

  Serial.print("Angulo="); 
  Serial.println(Delta);
  Serial.print("Intesidad");
  Serial.println(IntensidadActual);
  delay(500);  
  
  if (IntensidadActual > IntensidadPrevia) //Si aumento la intensidad
  {
    
  servo1.write(Delta+1);
  Delta = Delta + 1;
  delay(500);
  }
  else
  {
  servo1.write(Delta-1);
  Delta = Delta-1;
  delay(500); 
  } 
}
