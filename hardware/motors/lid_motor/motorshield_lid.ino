#include <Wire.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield();      // Motor shield object
Adafruit_StepperMotor *myMotor = AFMS.getStepper(200,2);  // Stepper Motor w 200 step per rev at M3 & M4

//Set pin, this is signal from RasPi to open lid
int inPin = 13;
int val = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Go Go Stepper Motor!!");
  AFMS.begin();
  myMotor->setSpeed(25);

  //Declare the pin for input
  pinMode(inPin, INPUT);
}

void loop() {
  
  val = digitalRead(inPin);
  Serial.println(val);
  if (val) {
    myMotor->step(50, FORWARD, SINGLE);
    delay(5000);
    myMotor->step(50, BACKWARD, SINGLE);
    delay(5000);
  }
  
  /*
  myMotor->step(100, FORWARD);
  delay(5000);
  myMotor->step(100, BACKWARD);
  delay(5000);
  */
  /*
  Serial.println("Two steps forward two steps back");
  myMotor->step(100, FORWARD, DOUBLE);
  myMotor->step(100, BACKWARD, DOUBLE);
  */
}

