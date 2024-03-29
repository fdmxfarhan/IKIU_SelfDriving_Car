#include <Servo.h>
Servo steeringServo;

int steer = 0;
int v = 0;
char recv;
int buff, cnt = 0;
int a = 1;
void motor(int v){
  if(v >= 0){
    digitalWrite(2, 0);
    digitalWrite(4, 1);
    analogWrite(3, v);
  }
  else{
    digitalWrite(2, 1);
    digitalWrite(4, 0);
    analogWrite(3, -v);
  }
}
void setup() {
  steeringServo.attach(5);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    recv = Serial.read();
    if (recv == 'J') {
      int val = 0;
      while (buff != '\n') {
        // delay(10);
        if (Serial.available() > 0) {
          buff = Serial.read();
          if (buff != '\n' && buff >= '0' && buff <= '9') {
            val = val * 10 + (buff - '0');

          }
        }
      }
      buff = ' ';
      steer = val-40;
    }
    if (recv == 'F') v = 255;
    if (recv == 'S') v = 0;
    if (recv == 'G') v = -255;

  }
  motor(v);
  steeringServo.write(90 + steer);


  //////////////////// Steering Test
  // steer += a;
  // if(steer >= 40 || steer <= -40) a = -a;
  // delay(30);
  
  //////////////////// Motor Test
  // v+=a;
  // if(v >= 255 || v <= -255) a = -a;
  // delay(5);
  
  //////////////////// Print Test
  // Serial.print("V:");
  // Serial.print(v);
  // Serial.print("  Steer:");
  // Serial.println(steer);

}
