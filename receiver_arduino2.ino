#include <Wire.h>
#include <Servo.h>

int pos = 0;
Servo servonum_left;
Servo servonum_right;

//declare the servos for the sliders 
Servo left1;
Servo right1;
Servo left2;
Servo right2;

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
  
  left1.attach(2);
  right1.attach(3);
  left2.attach(4);
  right2.attach(5);

  left1.write(90);
  right1.write(90);
  left2.write(90);
  right2.write(90);
}

void loop() {
  if (Serial.available() >0) {
  //from RPi to Mega
    r = Serial.read();
    Serial.println(r);
  }

  if ( r == '1' ) {
    Servo servonum_left = left1;
    Servo servonum_right = right1; 
    gateRelease(servonum_left, servonum_right); 
    Serial.write('3');
    r = '0';
    }
    
  if (r == '2') {
    Servo servonum_left = left2;
    Servo servonum_right = right2;
    gateRelease(servonum_left, servonum_right); 
    Serial.write('4');
    r = '0';
    }

}
