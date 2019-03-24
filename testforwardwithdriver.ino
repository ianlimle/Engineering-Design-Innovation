#include <ArduinoJson.h>
//#######################################
//#######################################
// GPIO mappings for Arduino Mega 2560
//#######################################
int m1_EL_Start_Stop=5;  //EL 
int m1_Signal_hall=3;   // Signal - Hall sensor
int m1_ZF_Direction=4;  // ZF 
int m1_VR_speed=9;    //VR 
int IN1 = 12 ;
int speed1= 10;
//#######################################
//#######################################
//int pos=0;int steps=0;int speed1=0;
String direction1;
//#######################################
//#######################################
/*void plus() {
  pos++; //count steps
  Serial.println(pos);
    if(pos>=steps){
      wheelStop();
      pos=0;
  }
}*/


void setup() {

// put your setup code here, to run once:
Serial.begin(9600);

//wheel 1 - Setup pin mode
pinMode(m1_EL_Start_Stop, OUTPUT);//stop/start - EL 
pinMode(m1_Signal_hall, INPUT);   //plus       - Signal  
pinMode(m1_ZF_Direction, OUTPUT); //direction  - ZF 
//pinMode(m1_VR_speed, OUTPUT);
pinMode(IN1,OUTPUT);
//Hall sensor detection - Count steps
// attachInterrupt(digitalPinToInterrupt(m1_Signal_hall), plus, CHANGE);

    
}


/*void drive(){
// {"direction":"forward","steps":"30","speed":"50"}
// {"direction":"backword","steps":"30","speed":"50"}
// {"direction":"stop","steps":"0","speed":"0"}--
 
      if(direction1=="forward" && pos<steps){
        //wheelMoveForward();
      }else if(direction1=="backword" && pos<steps){
        wheelMoveBackward();
      }else{
        Serial.println("Stop");
        wheelStop();
        pos=0;
      }        
 }*/
void wheelStop(){
  digitalWrite(m1_EL_Start_Stop,LOW);
}

void wheelMoveForward(){       
      
      digitalWrite(m1_ZF_Direction,HIGH);
      digitalWrite(m1_EL_Start_Stop,HIGH);
      digitalWrite(IN1,HIGH);
      analogWrite( m1_VR_speed ,speed1);
}

void wheelMoveBackward(){       
      digitalWrite(m1_ZF_Direction,LOW);
      digitalWrite(m1_EL_Start_Stop,HIGH);
      digitalWrite(IN1 ,HIGH);
      analogWrite( m1_VR_speed ,speed1);
      
}


void loop() {
  for(int i=1; i<=10; i++){
  wheelMoveForward();
  Serial.println(speed1);

  
  delay(2500);
  speed1 += 10 ;
  }
  
  speed1 = 10;
  for(int i=1; i<=10; i++){
  wheelMoveBackward();
  Serial.println(speed1);
  delay(2500);
  speed1 += 10 ;
  }
  wheelStop();
  exit(0);
}
