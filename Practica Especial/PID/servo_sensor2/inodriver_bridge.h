//// ****** THIS FILE IS AUTOGENERATED ******
////
////          >>>> DO NOT CHANGE <<<<
////
/// 
///  Filename; C:\Users\Sabrina\PycharmProjects\Instrumentallantz\Practica Especial\final_pid.py
///  Source class: servo_sensor2
///  Generation timestamp: 2019-07-25T11:22:01.020290
///  Class code hash: 2aece2d1e1c6b174ff83a52b98081c3b9099e601
///
/////////////////////////////////////////////////////////////

#ifndef inodriver_bridge_h
#define inodriver_bridge_h

#include <Arduino.h>

#include "SerialCommand.h"

#include "inodriver_user.h"

const char COMPILE_DATE_TIME[] = __DATE__ " " __TIME__;

void ok();
void error(const char*);
void error_i(int);
void bridge_loop();
void bridge_setup();

void getInfo();
void unrecognized(const char *);
void wrapperGet_Brillo(); 
void wrapperSet_Brillo(); 
void wrapperGet_Tiempo(); 
void wrapperSet_Tiempo(); 
void wrapperGet_Angulo(); 
void wrapperSet_Angulo(); 


#endif // inodriver_bridge_h