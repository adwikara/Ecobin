#include <Stepper.h>

// change this to the number of steps on your motor
#define STEPS 200

// create an instance of the stepper class, specifying
// the number of steps of the motor and the pins it's
// attached to
Stepper stepper(STEPS, 4, 5, 6, 7);

//Set pin, this is signal from RasPi to open lid
int inPin = 8;
int val = 0;

void setup()
{
  Serial.begin(9600);
  
  // set the speed of the motor to 10 RPMs
  stepper.setSpeed(10);

  //Declare the pin for input
  pinMode(inPin, INPUT);
  //pinMode(8, OUTPUT);
}

void loop()
{
  //digitalWrite(8, LOW);
  val = digitalRead(inPin);
  Serial.println(val);
  if (val) {
    //Serial.println("Forward");
    stepper.step(STEPS);
  }
  //Serial.println("Backward");
  //stepper.step(-STEPS);
}
