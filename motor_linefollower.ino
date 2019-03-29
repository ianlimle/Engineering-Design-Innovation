#include <QTRSensors.h>

#define Kp 0.08 //experiment to determine this, start with something small to make your bot follow the line at a slow speed
#define Kd 0.36 //experiment to determine this, slowly increase the speed to adjust the value
#define rightMaxSpeed 100
#define leftMaxSpeed 100
#define rightBaseSpeed 10 //speed at which motor should spin when robot is perfectly on line
#define leftBaseSpeed 10  //speed at which motor should spin when robot is perfectly on line
#define NUM_SENSORS 7
#define TIMEOUT 2500 //waits for 2500us for sensor outputs to go low
#define NUM_SAMPLES_PER_SENSOR 4
#define EMITTER_PIN 2 //emitter is controlled by digital pin 2


int left_EL_Start_Stop = 3;  //EL 
int left_Signal_hall = 4;   // Signal - Hall sensor
int left_ZF_Direction = 5;  // ZF
int leftMotor = 9; 
int IN1 = 11 ;

int right_EL_Start_Stop = 6;  //EL 
int right_Signal_hall = 7;   // Signal - Hall sensor
int right_ZF_Direction = 8;  // ZF 
int rightMotor = 10;
int IN3 = 12 ;

int lastError =0;


// Function QTRSensorsAnalog(unsigned char[], {sensor pin list}, NUM_SENSORS, NUM_SAMPLES_PER_SENSOR, EMITTER_PIN)
QTRSensorsAnalog qtra ((unsigned char[]) {,A5,A4,A3,A2,A1} ,NUM_SENSORS, NUM_SAMPLES_PER_SENSOR, EMITTER_PIN); 

unsigned int sensorValues[NUM_SENSORS];

void calibratesensor() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // turn on Arduino's LED to indicate we are in calibration mode
  // analogRead() takes about 0.1 ms on an AVR.
  // 0.1 ms per sensor * 4 samples per sensor read (default) * 4 sensors
  // * 10 reads per calibrate() call = ~24 ms per calibrate() call.
  // Call calibrate() 400 times to make calibration take about 10 seconds.
  for (uint16_t i = 0; i < 400; i++)
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
}

void Stop(){
  digitalWrite(left_EL_Start_Stop, LOW);
  digitalWrite(right_EL_Start_Stop, LOW);
}

void MoveForward(int leftSpeed, int rightSpeed){       
      
      digitalWrite(left_ZF_Direction, HIGH);
      digitalWrite(left_EL_Start_Stop, HIGH);
      digitalWrite(IN1, HIGH);
      analogWrite(leftMotor, leftSpeed);

      digitalWrite(right_ZF_Direction, HIGH);
      digitalWrite(right_EL_Start_Stop, HIGH);
      digitalWrite(IN3, HIGH);
      analogWrite(rightMotor, rightSpeed);
      
}

void MoveBackward(int leftSpeed, int rightSpeed){       
      digitalWrite(left_ZF_Direction, LOW);
      digitalWrite(left_EL_Start_Stop, HIGH);
      digitalWrite(IN1, HIGH);
      analogWrite(leftMotor, leftSpeed);

      digitalWrite(right_ZF_Direction, LOW);
      digitalWrite(right_EL_Start_Stop, HIGH);
      digitalWrite(IN3, HIGH);
      analogWrite(rightMotor, rightSpeed);
}


void setup() {
  Serial.begin(9600);  //initialize the baud rate
  
  pinMode(left_EL_Start_Stop, OUTPUT);//stop/start - EL 
  pinMode(left_Signal_hall, INPUT);   //plus       - Signal  
  pinMode(left_ZF_Direction, OUTPUT); //direction  - ZF 
  pinMode(IN1,OUTPUT);

  pinMode(right_EL_Start_Stop, OUTPUT);//stop/start - EL 
  pinMode(right_Signal_hall, INPUT);   //plus       - Signal  
  pinMode(right_ZF_Direction, OUTPUT); //direction  - ZF 
  pinMode(IN3,OUTPUT);
    
  calibratesensor() ;
  Serial.println("calibration done..");
}


void loop() {
  
  Serial.print("Analog \t");
  Serial.print(sensorValues[0]);
  Serial.print('\t');
  Serial.print(sensorValues[1]);
  Serial.print('\t');
  Serial.print(sensorValues[2]);
  Serial.print('\t');
  Serial.print(sensorValues[3]);
  Serial.print('\t');
  Serial.print(sensorValues[4]);
  Serial.print("\n");
  
  int position = qtra.readLine(sensorValues);
  Serial.println("position");
  Serial.print(position);
  Serial.print("\n");
  int error = position - 2000;
  Serial.println("error");
  Serial.print(error);
  Serial.print("\n");
  
  int motorSpeedAdjust = Kp * error + Kd * (error - lastError);
  
  //Serial.println(motorSpeedAdjust);
  lastError = error;

  //Compute augmented speeds for motor 
  int leftSpeed = (leftBaseSpeed - motorSpeedAdjust);
  Serial.println("leftSpeed");
  Serial.print(leftSpeed);
  Serial.print("\n");
  
  int rightSpeed = 0.9*(rightBaseSpeed + motorSpeedAdjust);
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
  MoveForward(leftSpeed, rightSpeed);

  /*if sensors read all white, meaning end of line
   * 
   * Stop();
   * 
   */

}

