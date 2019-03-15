#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#include <EEPROM.h> 
#include <ESP8266WiFi.h> //library for the ESP8266 to connect to a WiFi network
#include <PubSubClient.h> //library for the ESP8266 to connect to a MQTT broker and publish/subscribe messages in topics
#include <WiFiClient.h> 

#define SERVOMIN_90  300 // this is the 'minimum' pulse length count for a 90 degree angle
#define SERVOMAX_90  450 // this is the 'maximum' pulse length count for a 90 degree angle
 
#define SERVOMIN_180 150 // this is the 'minimum' pulse length count for a 180 degree angle
#define SERVOMAX_180 600 // this is the 'maximum' pulse length count for a 180 degree angle

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
// you can also call it with a different address and I2C interface
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(&Wire, 0x40);

/* initialize servo counter
const int tier01_rack01_left = 0;
const int tier01_rack01_right = 1;

const int tier01_rack02_left = 3;
const int tier01_rack02_right = 4;

const int tier02_rack01_left = 6;
const int tier02_rack01_right = 7;

const int tier02_rack02_left = 9;
const int tier02_rack02_right = 10;
*/
int servonum_left;
int servonum_right;
char* pubTopic;

// declare global variables for wifi connections 
const char* ssid = "...wifissid";
const char* password = "...wifipassword";

// declare information for MQTT Server
const char* mqttServer = "....."; //server address
const int mqttPort = 1883; //server port
const char* mqttUser = "....."; //server user
const char* mqttPass = "....."; //server password

WiFiClient espClient;
PubSubClient client(espClient);

void reconnect() {
  //loop until connected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    //attempt to connect
    if (client.connect("ESP8266Client", mqttUser, mqttPass)) {
      Serial.print("connected");
      //and subscribe to topic
      client.subscribe("11");
      client.subscribe("12");
      client.subscribe("21");
      client.subscribe("22");
    } 
    else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      //wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned length) {
  Serial.print("Message topic: ");
  Serial.print(topic);
  
  for (int i=0; i < length; i++) {
    char receivedChar = (char)payload[i];
    Serial.println(receivedChar);
  }
  //payload[length] = '\0'; //terminate string with '0' 
  String strPayload = String((char*)payload); //convert to string
  Serial.println(strPayload);
  
  String strTopic = String((char*)topic); 
  if (strTopic == (char*)'11') {
    const int servonum_left = 0;
    const int servonum_right = 1;
    char* pubTopic = (char*)'111';
  }
  if (strTopic == (char*)'12') {
    const int servonum_left = 3;
    const int servonum_right = 4;
    char* pubTopic = (char*)'121';
  }
  if (strTopic == (char*)'21') {
    const int servonum_left = 6;
    const int servonum_right = 7;
    char* pubTopic = (char*)'211';
  }
  if (strTopic == (char*)'22') {
    const int servonum_left = 9;
    const int servonum_right = 10;
    char* pubTopic = (char*)'221';
  }
  

  if (strPayload == (char*)'1')  {
     for (uint16_t pulselen = SERVOMIN_90; pulselen < SERVOMAX_90; pulselen++) {
      pwm.setPWM(servonum_left, 0, pulselen);  
      pwm.setPWM(servonum_right, 0, pulselen);
     }
     delay(500);
     pwm.setPWM(servonum_left, 4096, 0); //fully off the motor
     pwm.setPWM(servonum_right, 4096, 0);
     delay(2000); //delay the motor

     for (uint16_t pulselen = SERVOMAX_90; pulselen > SERVOMIN_90; pulselen--) {
      pwm.setPWM(servonum_left, 0, pulselen);
      pwm.setPWM(servonum_right, 0, pulselen);
     }
     delay(500);
     pwm.setPWM(servonum_left, 4096, 0); //fully off the motor 
     pwm.setPWM(servonum_right, 4096, 0);
     delay(2000); //delay the motor

     client.publish(pubTopic, (char*)'Gate Release Done'); //publish to RPi robot for confirmation on slider release
  }   
}

void setup() {
  
  Serial.begin(9600); //initialize the baud rate of the serial monitor
  WiFi.begin(ssid, password); //initialize connection to wifi network

  client.setServer(mqttServer, mqttPort); // set the 
  client.setCallback(callback); // set the callback function to trigger when messages are received from the broker
  
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  delay(10);

}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  
  client.loop(); //allow client process incoming messages and maintain its connection to the server
  
}
