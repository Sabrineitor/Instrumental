//// ****** THIS FILE IS AUTOGENERATED ******
////
////          >>>> DO NOT CHANGE <<<<
////
/// 
///  Filename; C:\Users\Sabrina\PycharmProjects\Instrumentallantz\Practica Especial\final_pid.py
///  Source class: servo_sensor2
///  Generation timestamp: 2019-07-25T11:22:01.157470
///  Class code hash: 2aece2d1e1c6b174ff83a52b98081c3b9099e601
///
/////////////////////////////////////////////////////////////



// Import libraries
#include <Arduino.h>

#include "inodriver_bridge.h"
#include "inodriver_user.h"

#define BAUD_RATE 9600

void setup() {
  bridge_setup();
  
  user_setup();

  Serial.begin(BAUD_RATE);
}

void loop() {
  
  bridge_loop();
  
  user_loop();
}
