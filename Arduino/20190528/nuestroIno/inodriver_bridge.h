//// ****** THIS FILE IS AUTOGENERATED ******
////
////          >>>> DO NOT CHANGE <<<<
////
/// 
///  Filename; C:\Users\realm.DESKTOP-DQ0IJ8Q\Documents\GitHub\instrumentacion\20190528\nuestroduino.py
///  Source class: nuestroIno
///  Generation timestamp: 2019-05-28T19:20:09.319187
///  Class code hash: 8772586d05ab6f0f6d3c4d62f2453d258ff96180
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
void wrapperGet_LIGHT(); 
void wrapperSet_LIGHT(); 


#endif // inodriver_bridge_h