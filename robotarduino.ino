#include <QTRSensors.h>
#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <Servo.h>


#define Kp 0.18//experiment to determine this, start with something small to make your bot follow the line at a slow speed
#define Kd 0.25  //experiment to determine this, slowly increase the speed to adjust the value
#define Kp1 0.15


//experiment to determine this, start with something small to make your bot follow the line at a slow speed
#define Kd1 0.23//experiment to determine this, slowly increase the speed to adjust the value
int rightMaxSpeed = 60;
//#define leftMaxSpeed_100 0
int leftMaxSpeed = 50 ;
int rightBaseSpeed = 40; //speed at which motor should spin when robot is perfectly on line
int leftBaseSpeed = 30;  //speed at which motor should spin when robot is perfectly on line
#define NUM_SENSORS  7
#define TIMEOUT 2500 //waits for 2500us for sensor outputs to go low
#define NUM_SAMPLES_PER_SENSOR 4
#define EMITTER_PIN 2 //emitter is controlled by digital pin 2
#include <Adafruit_NeoPixel.h>
#include<SPI.h> 
#define LED_COUNT 30
#define LED_PIN 13


//left
int left_EL_Start_Stop = 26;  //EL 
int left_Signal_hall = 24;   // Signal - Hall sensor
int left_ZF_Direction = 22;  // ZF
int leftMotor = 5; 
int IN1 = 6 ;
//right
int right_EL_Start_Stop = 52;  //EL 
int right_Signal_hall = 50;   // Signal - Hall sensor
int right_ZF_Direction = 48;  // ZF 
int rightMotor = 9;
int IN4 = 8 ;
int relaypin = 30;
int relaypin1 = 31;
int limitswitch = 32;
int countererror;
int lastError ; 
int count; // count for loops run
int i;//count for led delay
int robotstate; //changed based on serial read
char r; //variablee for serial.read
int state ;
int innerstate; 
int innerstate0;
uint32_t color = 0x00ff00;
uint16_t start = 0;
uint16_t finish = 30;
uint16_t len = 2;
int val = 0; //value of limit switch

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN);
// Function QTRSensorsAnalog(unsigned char[], {sensor pin list}, NUM_SENSORS, NUM_SAMPLES_PER_SENSOR, EMITTER_PIN)
//QTRSensorsAnalog qtra ((unsigned char[]) {A0,A1,A2,A3,A4,A5,A6} ,NUM_SENSORS, NUM_SAMPLES_PER_SENSOR, EMITTER_PIN); 
const int sensors[7] = {A0,A1,A2,A3,A4,A5,A6};
unsigned int sensorValues[NUM_SENSORS];
int dgsensorValues[7];


int pos = 0;
//declare the servos for the sliders 
Servo left;
Servo right;
/*void myreadLine(int sensorValues[], int 7){
 
  int ans = (0*sensorValues[0]+1000*sensorValues[1]+2000*sensorValues[2]+3000*sensorValues[3]+4000*sensorValues[4]+5000*sensorValues[5]+6000*sensorValues[6]);
  int ans2 = sensorValues[0]+sensorValues[1]+sensorValues[2]+sensorValues[3]+sensorValues[4]+sensorValues[5]+sensorValues[6];
  int finalans = ans/ans2 ;
  //return finalans ;
}*/
void bounceBetween(uint32_t color, uint16_t start, uint16_t finish, uint16_t len, int i){
  
  int path_length = finish - start;
  //Get the light snake move forward down the strip
   Serial.println( "i");
   Serial.println(i);
    //Populate the snake
    for (int j=0 ; j < len; j++){
      strip.setPixelColor(i+j+start, color);
      strip.show();
    }
    
    if (((i+start) <= (finish-len+1))){
      strip.setPixelColor(i+start,0);
      
  }
}  
/*void calibratesensor() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // turn on Arduino's LED to indicate we are in calibration mode
  // analogRead() takes about 0.1 ms on an AVR.
  // 0.1 ms per sensor * 4 samples per sensor read (default) * 4 sensors
  // * 10 reads per calibrate() call = ~24 ms per calibrate() call.
  // Call calibrate() 400 times to make calibration take about 10 seconds.
  for (int i = 0; i < 400; i++)
  {
    qtra.calibrate();
  }
  digitalWrite(LED_BUILTIN, LOW); // turn off Arduino's LED to indicate we are through with calibration

 
  for (int i = 0; i < NUM_SENSORS; i++)
    {
      Serial.print(qtra.calibratedMinimumOn[i]);
      Serial.print(' ');
    }
    Serial.println();

    for (int i = 0; i < NUM_SENSORS; i++)
    {
      Serial.print(qtra.calibratedMaximumOn[i]);
      Serial.print(' ');
    }
    Serial.println();
    
}*/

void Stop(){
  digitalWrite(left_EL_Start_Stop, LOW);
  digitalWrite(right_EL_Start_Stop, LOW);
}

void MoveForward(int leftSpeed_PWM, int rightSpeed_PWM){       
      
      digitalWrite(left_ZF_Direction, HIGH);
      digitalWrite(left_EL_Start_Stop, HIGH);
      digitalWrite(IN1, HIGH);
      analogWrite(leftMotor, leftSpeed_PWM);

      digitalWrite(right_ZF_Direction, LOW);
      digitalWrite(right_EL_Start_Stop, HIGH);
      digitalWrite(IN4, HIGH);
      analogWrite(rightMotor, rightSpeed_PWM);
      
}

void MoveBackward(int leftSpeed_PWM, int rightSpeed_PWM){       
      digitalWrite(left_ZF_Direction, LOW);
      digitalWrite(left_EL_Start_Stop, HIGH);
      digitalWrite(IN1, HIGH); 
      analogWrite(leftMotor, leftSpeed_PWM);

      digitalWrite(right_ZF_Direction, HIGH);
      digitalWrite(right_EL_Start_Stop, HIGH);
      digitalWrite(IN4, HIGH);
      analogWrite(rightMotor, rightSpeed_PWM);
}
void Turn(int leftSpeed_PWM, int rightSpeed_PWM){       
      
      digitalWrite(left_ZF_Direction, HIGH);
      digitalWrite(left_EL_Start_Stop, HIGH);
      digitalWrite(IN1, HIGH);
      analogWrite(leftMotor, leftSpeed_PWM);

      digitalWrite(right_ZF_Direction, HIGH);
      digitalWrite(right_EL_Start_Stop, HIGH);
      digitalWrite(IN4, HIGH);
      analogWrite(rightMotor, rightSpeed_PWM);
      
}

void setup() {
  Serial.begin(9600);  //initialize the baud rate
  Serial.println("state");
  Serial.println(state);
  strip.begin();
  strip.show();
  //leftwheel
  pinMode(left_EL_Start_Stop, OUTPUT);//stop/start - EL 
  pinMode(left_Signal_hall, INPUT);   //plus       - Signal  
  pinMode(left_ZF_Direction, OUTPUT); //direction  - ZF 
  pinMode(IN1,OUTPUT);
  //rightwheel
  pinMode(right_EL_Start_Stop, OUTPUT);//stop/start - EL 
  pinMode(right_Signal_hall, INPUT);   //plus       - Signal  
  pinMode(right_ZF_Direction, OUTPUT); //direction  - ZF 
  pinMode(IN4,OUTPUT);
  pinMode(relaypin, OUTPUT);
  pinMode(relaypin1, OUTPUT);
  pinMode(limitswitch,INPUT);  
  digitalWrite(relaypin,HIGH);
  digitalWrite(relaypin1,HIGH);
  //Servo
  left.attach(11); //pinnumber for leftservo
  right.attach(12);//pinnumber for rightservo
  left.write(90);
  right.write(90);
  //instances
  count = 0;
  i = 0;
  state = 0 ;
  innerstate = 1;
  innerstate0 = 1;
  robotstate = 0;
}

void gateReleaseCCW(Servo myservo1,Servo myservo2) {
   for (pos = 0; pos <= 180; pos += 1) { //call servos to shift in direction
     myservo1.write(pos);
     myservo2.write(pos);              
    }
   delay(450);
   myservo1.write(90);//servo to stop 
   myservo2.write(90);
   delay(3000);   //delay for 3 seconds
    
   for (pos = 180; pos >= 0; pos -= 1) { //call servos to shift in the opposite direction 
     myservo1.write(pos);    
     myservo2.write(pos);                                  
    }
   delay(450);
   myservo1.write(90); //servo to stop
   myservo2.write(90);
   //delay(3000);      //delay for 3 seconds
  }
  
void fromrack() {
  
  /*if (count == 22  && state == 1){
    MoveForward(10,50);
    }
  if (count == 20  && state == 1){
    digitalWrite(relaypin,LOW);}*/
    if (count % 1 == 0){
    if (i == 30){  
      i=0;
    }
    else{
    i += 1; 
  }
  }
  bounceBetween(color,start,finish,len,i);
  while ( true ) {
  for ( int i=0;i< NUM_SENSORS; i++)
  {
  sensorValues[i] = analogRead(sensors[i]);
  Serial.print(sensorValues[i]);
  Serial.print('\t');
 }
 
  for (int i = 0; i < NUM_SENSORS ; i++)
  { if( sensorValues[i] >= 700 ){ 
    
     
     dgsensorValues[i] = 1 ;
  }
  else{ 
    dgsensorValues[i] = 0 ;
  }
    //Serial.print(sensorValues[i]);
    Serial.print(dgsensorValues[i]);
    Serial.print('\t');
    
  }
 // myreadLine(sensorValues);
  //Serial.pri nt(dgsensorValues[1]);
  int ans = (-3*dgsensorValues[0]-2*dgsensorValues[1]-1*dgsensorValues[2]+0*dgsensorValues[3]+1*dgsensorValues[4]+2*dgsensorValues[5]+3*dgsensorValues[6]);
  int ans2 = dgsensorValues[0]+dgsensorValues[1]+dgsensorValues[2]+dgsensorValues[3]+dgsensorValues[4]+dgsensorValues[5]+dgsensorValues[6];
  Serial.println(ans2);
  int finalans = ans/ans2 ;
  int position = finalans;
  Serial.println("finalans");
  Serial.print(finalans);
  Serial.print("\n"); 
  int error = 100*position ;
  Serial.println("error");
  Serial.print(error);
  Serial.print("\n");
  
     
  int motorSpeedAdjust = Kp * error + Kd * (error - lastError);
  int motorSpeedAdjust_left = Kp1 * error + Kd1 * (error-lastError);
  //Serial.println(motorSpeedAdjust);
  lastError = error;

  //Compute augmented speeds for motor 
  int leftSpeed = (leftBaseSpeed - motorSpeedAdjust_left);
  
  Serial.println("leftSpeed");
  Serial.print(leftSpeed);
  Serial.print("\n");
  
  int rightSpeed = (rightBaseSpeed + motorSpeedAdjust);
  
  Serial.println("rightSpeed");
  Serial.print(rightSpeed);
  Serial.print("\n"); 
  
  //Set limits
  if (leftSpeed > leftMaxSpeed) {
    leftSpeed = leftMaxSpeed; 
  } 
  if (rightSpeed > rightMaxSpeed) {
    rightSpeed = rightMaxSpeed;
  }
  if (leftSpeed < 0) {
    leftSpeed = 0;
  }
  if (rightSpeed < 0) {
    rightSpeed = 0;
  }


  //move forward
  int leftSpeed_PWM = leftSpeed*0.35;
  int rightSpeed_PWM = rightSpeed*0.6;
  /* if (state == 0){
      if (ans2 == 7){
       state = 1 ;
       MoveForward(5,5);
       Serial.println("changestate");
       Serial.println(state);
       break;
       }
      else {
        MoveForward(leftSpeed_PWM, rightSpeed_PWM);
        state = 0 ;
        Serial.println("remainstate");
        Serial.println(state);
        break;
       } 
  }*/
  if (state == 0) {
    if (count == 25) {
      MoveBackward(10,10);
      Serial.println("changetostate1");
      state = 1;
      innerstate0 = 1;
      break;
    }
    if (count == 20) {
      digitalWrite(relaypin,LOW);
      MoveBackward(10,10);
      break;
    }
    else{
    MoveBackward(10,10);
    break;
    }
  }
  if (state == 1) {
    if (innerstate0 == 1){
      MoveBackward(10,10);
      Serial.println("reversing");
      delay(3000);
      MoveForward(0,30);
      delay(1000);
      innerstate0 = 2;
      break;
    }
    
    if (innerstate0 == 2 && (dgsensorValues[4] + dgsensorValues[5] >= 1)){
     digitalWrite(relaypin,HIGH); 
     Serial.println("stopforawhile");
     count = 0;
     state = 2;
     break;
    }
    if (innerstate0 == 2 && (dgsensorValues[5] + dgsensorValues[6] == 0)){
     MoveForward(0,25 );
     Serial.println("Turning");
      break;
    }
  }
  if (state == 2) {
    if (count == 25) {
      state = 3;
      break;
    }
    if (count == 20) {
      digitalWrite(relaypin,LOW);
      MoveForward(10,10);
      break;
    }
    MoveForward(10,10);
    break;
    
  }
  if (state == 3){
      if (ans2 == 7){
       state = 4 ;
       MoveForward(5,5);
       Serial.println("changestate");
       Serial.println(state);
       break;
       }
      else {
        MoveForward(leftSpeed_PWM, rightSpeed_PWM);
        Serial.print("Movinn");
        state = 3 ;
        Serial.println("remainstate");
        Serial.println(state);
        break;
       } 
  }
  if ( state == 4 ) {
      if (ans2 == 7){
        MoveForward(5,5); 
        state = 4 ;
        break;
        }
      if (ans2 != 7){ 
        //lastError = 0 ;
        state = 5 ;
        Serial.println("changestate");
        Serial.println(state);
        break;
      }
  }
  if (state == 5){
    Serial.println("innerstate");
    Serial.println(innerstate);
    if (((dgsensorValues[5] + dgsensorValues[6]) >= 1) &&((dgsensorValues[0]+ dgsensorValues[1]+ dgsensorValues[2] + dgsensorValues[3] + dgsensorValues[4] )== 0 )&& (innerstate != 1)){
      Serial.println("gonnaturnleft");
      innerstate = 1 ;
      break ;
    }
    if (((dgsensorValues[0] + dgsensorValues[1]) >= 1) &&((dgsensorValues[2]+ dgsensorValues[3]+ dgsensorValues[4] + dgsensorValues[5] + dgsensorValues[6] )== 0 )&& (innerstate != 2)) {
      Serial.println("gonnaturnright");
      innerstate = 2;
      break;
    }
    if (ans2 == 0 && innerstate == 1) {
      Serial.print("turning");
      MoveForward(5,35); 
      break ;
      }
    if (ans2 == 0 && innerstate == 2) {
      Serial.print("turningright");
      MoveForward(20,5); 
      break ;
      }
    if (ans2 == 7) {
      MoveForward (1,1) ; 
      Serial.println("changestateto4");
      state = 6 ;
      break;
    }
    else {
      Serial.print("movin normally");
      MoveForward(leftSpeed_PWM, rightSpeed_PWM);
      break;
     }
  }
  if (state == 6) {
    if (ans2 == 7) {
    MoveForward (2,2) ;
    break;   
    }
   else {
      rightMaxSpeed = 25;
      leftMaxSpeed = 25 ;
      rightBaseSpeed = 10;
      leftBaseSpeed =  10 ; 
      state = 7;
      break;
      
    }
  }
  if ( state == 7) {
    if (ans2 == 7) {
     digitalWrite(relaypin,HIGH);
     count = 0;
     state = 0;
     robotstate = 0;
     Serial.write('4');
     break; 
    }
     else{
      MoveForward(leftSpeed_PWM, rightSpeed_PWM);
     }
     break;
  }
  
  
  /*if sensors read all white, meaning end of line
   * 
   * Stop();
   * 
   */

  }
  count += 1;
  Serial.println("count");
  Serial.println(count);
  Serial.println("state");
  Serial.println(state);
}


void torack() {
  
  /*if (count == 22  && state == 1){
    MoveForward(10,50);
    }
  if (count == 20  && state == 1){
    digitalWrite(relaypin,LOW);}*/
    
  // digitalWrite(relaypin,LOW);
    if (count % 1 == 0){
    if (i == 30){
      i=0;
    }
    else{
    i += 1; 
  }
  }
  while ( true ) {
  for ( int i=0;i< NUM_SENSORS; i++)
  {
  sensorValues[i] = analogRead(sensors[i]);
  Serial.print(sensorValues[i]);
  Serial.print('\t');
 }
 
  for (int i = 0; i < NUM_SENSORS ; i++)
  { if( sensorValues[i] >= 700 ){ 
    
     
     dgsensorValues[i] = 1 ;
  }
  else{ 
    dgsensorValues[i] = 0 ;
  }
    //Serial.print(sensorValues[i]);
    Serial.print(dgsensorValues[i]);
    Serial.print('\t');
    
  }
 // myreadLine(sensorValues);
  //Serial.pri nt(dgsensorValues[1]);
  int ans = (-3*dgsensorValues[0]-2*dgsensorValues[1]-1*dgsensorValues[2]+0*dgsensorValues[3]+1*dgsensorValues[4]+2*dgsensorValues[5]+3*dgsensorValues[6]);
  int ans2 = dgsensorValues[0]+dgsensorValues[1]+dgsensorValues[2]+dgsensorValues[3]+dgsensorValues[4]+dgsensorValues[5]+dgsensorValues[6];
  Serial.println(ans2);
  int finalans = ans/ans2 ;
  int position = finalans;
  Serial.println("finalans");
  Serial.print(finalans);
  Serial.print("\n"); 
  int error = 100*position ;
  Serial.println("error");
  Serial.print(error);
  Serial.print("\n");
  
     
  int motorSpeedAdjust = Kp * error + Kd * (error - lastError);
  int motorSpeedAdjust_left = Kp1 * error + Kd1 * (error-lastError);
  //Serial.println(motorSpeedAdjust);
  lastError = error;

  //Compute augmented speeds for motor 
  int leftSpeed = (leftBaseSpeed - motorSpeedAdjust_left);
  
  Serial.println("leftSpeed");
  Serial.print(leftSpeed);
  Serial.print("\n");
  
  int rightSpeed = (rightBaseSpeed + motorSpeedAdjust);
  
  Serial.println("rightSpeed");
  Serial.print(rightSpeed);
  Serial.print("\n"); 
  
  //Set limits
  if (leftSpeed > leftMaxSpeed) {
    leftSpeed = leftMaxSpeed; 
  } 
  if (rightSpeed > rightMaxSpeed) {
    rightSpeed = rightMaxSpeed;
  }
  if (leftSpeed < 0) {
    leftSpeed = 0;
  }
  if (rightSpeed < 0) {
    rightSpeed = 0;
  }


  //move forward
  int leftSpeed_PWM = leftSpeed*0.35;
  int rightSpeed_PWM = rightSpeed*0.6;
  /* if (state == 0){
      if (ans2 == 7){
       state = 1 ;
       MoveForward(5,5);
       Serial.println("changestate");
       Serial.println(state);
       break;
       }
      else {
        MoveForward(leftSpeed_PWM, rightSpeed_PWM);
        state = 0 ;
        Serial.println("remainstate");
        Serial.println(state);
        break;
       } 
  }*/
  if (state == 0) {
    if (count == 25) {
      state = 1;
      break;
    }
    if (count == 20) {
      digitalWrite(relaypin,LOW);
      MoveForward(10,10);
      break;
    }
    MoveForward(10,10);
    break;
    
  }
  if (state == 1){
      if (ans2 == 7){
       state = 2 ;
       MoveForward(5,5);
       Serial.println("changestate");
       Serial.println(state);
       break;
       }
      else {
        MoveForward(leftSpeed_PWM, rightSpeed_PWM);
        Serial.print("Movinn");
        state = 1 ;
        Serial.println("remainstate");
        Serial.println(state);
        break;
       } 
  }
  if ( state == 2 ) {
      if (ans2 == 7){
        MoveForward(5,5); 
        state = 2 ;
        break;
        }
      if (ans2 != 7){ 
        //lastError = 0 ;
        state = 3 ;
        Serial.println("changestate");
        Serial.println(state);
        break;
      }
  }
  if (state == 3){
    Serial.println("innerstate");
    Serial.println(innerstate);
    if (((dgsensorValues[5] + dgsensorValues[6]) >= 1) &&((dgsensorValues[0]+ dgsensorValues[1]+ dgsensorValues[2] + dgsensorValues[3] + dgsensorValues[4] )== 0 )&& (innerstate != 1)){
      Serial.println("gonnaturnleft");
      innerstate = 1 ;
      break ;
    }
    if (((dgsensorValues[0] + dgsensorValues[1]) >= 1) &&((dgsensorValues[2]+ dgsensorValues[3]+ dgsensorValues[4] + dgsensorValues[5] + dgsensorValues[6] )== 0 )&& (innerstate != 2)) {
      Serial.println("gonnaturnright");
      innerstate = 2;
      break;
    }
    if (ans2 == 0 && innerstate == 1) {
      Serial.print("turning");
      MoveForward(5,35); 
      break ;
      }
    if (ans2 == 0 && innerstate == 2) {
      Serial.print("turningright");
      MoveForward(20,5); 
      break ;
      }
    if (ans2 == 7) {
      MoveForward (2,2) ; 
      Serial.println("changestateto4");
      state = 4 ;
      break;
    }
    else {
      Serial.print("movin normally");
      MoveForward(leftSpeed_PWM, rightSpeed_PWM);
      break;
     }
  }
  if (state == 4) {
    if (ans2 == 7) {
    MoveForward (2,2) ;
    break;   
    }
   else {
      rightMaxSpeed = 25;
      leftMaxSpeed = 25 ;
      rightBaseSpeed = 10;
      leftBaseSpeed =  10 ; 
      state = 5 ;
      break;
      
    }
  }
  if ( state == 5) {
    if (ans2 == 7) {
     digitalWrite(relaypin,HIGH);
     count = 0;
     state = 0;
     robotstate = 0;
     Serial.write('2');
     break; 
    }
     else{
      MoveForward(leftSpeed_PWM, rightSpeed_PWM);
     }
     break;
  }
  
  
  /*if sensors read all white, meaning end of line
   * 
   * Stop();
   * s
   */

  }
  count += 1;
  Serial.println("count");
  Serial.println(count);
  Serial.println("state");
  Serial.println(state);
}

void loop() {
  val = digitalRead(limitswitch);
  while( true ){
    Serial.println(robotstate);
  if (Serial.available() >0 && robotstate == 0) {
  //from RPi to Mega
    r = Serial.read();
    String a = "";
    a += r;
    int b = a.toInt();
    Serial.println(b);
    robotstate = b;
    break;
  }

  if (robotstate == 1 && val == LOW) {
    Serial.println("startingtogo");
    torack();
    break;
    }
  if (robotstate == 3 &&  val == LOW){
    fromrack( ); 
    break;
  }
  if(robotstate == 5 &&  val == LOW){
    digitalWrite(relaypin1,LOW);
    gateReleaseCCW(left,right);
    //Serial.write('6');
    digitalWrite(relaypin1,HIGH);
    robotstate = 0;
    break;
  }
  if(val == HIGH){
    robotstate = 0;
    break;  
}
else {
Serial.println("idle");
}
}
}



  

  
