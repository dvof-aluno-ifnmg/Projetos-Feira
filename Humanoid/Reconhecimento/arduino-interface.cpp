#include <Servo.h>

Servo servo;  // create Servo object to control a servo
int val;
int lastval = 0;
void setup() {
  servo.attach(9);  // attaches the servo on pin 9 to the Servo object
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()){
    int lec = Serial.parseInt();
    val = constrain(lec,0,180);

    if (lastval < val) {
      for(int i = lastval; i <= val;i++){
      Serial.println(i);
      servo.write(i);                  // sets the servo position according to the scaled value
      delay(2); 
      }    
        lastval = val;
    }                      // waits for the servo to get there
    if (lastval > val) {
      for(int i = lastval; i >= val; i--){
      Serial.println(i);
      servo.write(i);                 // sets the servo position according to the scaled value
      delay(2); 
      } 
      lastval = val;
    }           
  }
}
