#include <Wire.h>
#include <Servo.h>

int pos = 0;
char r;
Servo servonum;

//declare the servos for the sliders 
Servo tier01_rack01;
Servo tier01_rack02;
Servo tier02_rack01;
Servo tier02_rack02;

void gateRelease(Servo myservo) {
   for (pos = 0; pos <= 180; pos += 1) { //call servos to shift in direction
     myservo.write(pos);             
    }
   delay(350);
   myservo.write(90); //left servo to stop 
   delay(3000);   //delay for 3 seconds
    
   for (pos = 180; pos >= 0; pos -= 1) { //call servos to shift in the opposite direction 
     myservo.write(pos);
   }
   delay(350);
   myservo.write(90); //right servo to stop
   delay(3000);      //delay for 3 seconds

  }


void setup() {
  
  Serial.begin(9600);
  
  tier01_rack01.attach(2);
  tier01_rack02.attach(3);
  tier02_rack01.attach(4);
  tier02_rack02.attach(5);

  tier01_rack01.write(90);
  tier01_rack02.write(90);
  tier02_rack01.write(90);
  tier02_rack02.write(90);
}


void loop() {
  if (Serial.available() >0) {
  //from RPi to Mega
    r = Serial.read();
    Serial.println(r);
  }
  
  if (r == '1' ) {
    Servo servonum = tier01_rack01; 
    gateRelease(servonum);
    Serial.write('5');
    r = '0';
    }
    
  if (r == '2') {
    Servo servonum = tier01_rack02;
    gateRelease(servonum);
    Serial.write('6');
    r = '0';
    }
    
  if (r == '3') {
    Servo servonum = tier02_rack01;
    gateRelease(servonum); 
    Serial.write('7');
    r = '0';
    }
    
  if (r == '4') {
    Servo servonum = tier02_rack02;
    gateRelease(servonum);
    Serial.write('8');
    r = '0';
    }
}
