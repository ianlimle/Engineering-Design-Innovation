#include <Wire.h>
#include <Servo.h>

int pos = 0;
Servo servonum_left;
Servo servonum_right;

Servo mysevoleft ;
Servo myservoright;

//declare the servos for the sliders 
Servo tier01_rack01_left;
Servo tier01_rack01_right;
Servo tier01_rack02_left;
Servo tier01_rack02_right;
Servo tier02_rack01_left;
Servo tier02_rack01_right;
Servo tier02_rack02_left;
Servo tier02_rack02_right;

char r;

void gateRelease(Servo myservoleft, Servo myservoright) {
   for (pos = 0; pos <= 180; pos += 1) { //call servos to shift in direction
     myservoleft.write(pos);
     myservoright.write(pos);              
    }
   delay(350);
   myservoleft.write(90); //left servo to stop 
   myservoright.write(90); //right servo to stop
   delay(3000);   //delay for 3 seconds
    
   for (pos = 180; pos >= 0; pos -= 1) { //call servos to shift in the opposite direction 
     myservoleft.write(pos);
     myservoright.write(pos);                                      
    }
   delay(350);
   myservoleft.write(90); //left servo to stop
   myservoright.write(90); //right servo to stop
   delay(3000);      //delay for 3 seconds
  }


void setup() {
  Serial.begin(9600);
  
  tier01_rack01_left.attach(2);
  tier01_rack01_right.attach(3);
  tier01_rack02_left.attach(4);
  tier01_rack02_right.attach(5);
  tier02_rack01_left.attach(8);
  tier02_rack01_right.attach(9);
  tier02_rack02_left.attach(7);
  tier02_rack02_right.attach(0);

  tier01_rack01_left.write(90);
  tier01_rack01_right.write(90);
  tier01_rack02_left.write(90);
  tier01_rack02_right.write(90);
  tier02_rack01_left.write(90);
  tier02_rack01_right.write(90);
  tier02_rack02_left.write(90);
  tier02_rack02_right.write(90); 
}

void loop() {
  if (Serial.available() >0) {
  //from RPi to Mega
    r = Serial.read();
    Serial.println(r);
  }
  
  if ( r == '1' ) {
    Servo servonum_left = tier01_rack01_left;
    Servo servonum_right = tier01_rack01_right; 
    gateRelease(servonum_left, servonum_right); 
    Serial.write('1');
    delay(100);
    r = '0';
    }
    
  if (r == '2') {
    Servo servonum_left = tier01_rack02_left;
    Servo servonum_right = tier01_rack02_right;
    gateRelease(servonum_left, servonum_right); 
    Serial.write('2');
    delay(100);
    r = '0';
    }
    
  if (r == '3') {
    Servo servonum_left = tier02_rack01_left;
    Servo servonum_right = tier02_rack01_right;
    gateRelease(servonum_left, servonum_right); 
    Serial.write('3');
    delay(100);
    r = '0';
    }
    
  if (r == '4') {
    Servo servonum_left = tier02_rack02_left;
    Servo servonum_right = tier02_rack02_right;
    gateRelease(servonum_left, servonum_right); 
    Serial.write('4');
    delay(100);
    r = '0';
    }
}
