//////
// core.ino - RasPiO Duino Program for motor control, line following
//////

// Servo library & initialising head servos
#include <Servo.h>
Servo pan;
Servo tilt;

// kazillions of variables
const int master_enable = 2;
const int led_pin = 13;
const int left_motor_forward = 3;
const int left_motor_backward = 4;
const int left_motor_enable = 5;
const int right_motor_enable = 6;
const int right_motor_forward = 7;
const int right_motor_backward = 8;
const int loop_pause = 10; // delay (ms) between: each loop cycle; jump to next stepped pwm value for left motor and right motor
int left_motor_value = 0;
int right_motor_value = 0;
int left_motor_aim = 0;
int right_motor_aim = 0;

const int pan_servo = 9;
const int tilt_servo = 10;
int tilt_ms = 1300;
int pan_ms = 1500;
boolean disabled = false;
boolean pi_ready = false;

// pin to test battery voltage, scaled through a voltage divider, and variable to hold battery voltage
int battery_voltage_pin = A0;
int battery_voltage = 0;

const int ultrasonic_echo = 11;
const int ultrasonic_trigger = 12;
float distance_cm = 0;

int ir_map[3] = {0, 0, 0}; //call to map_line() updates this to sensor readings. 0=LOW=dark, 1=HIGH=light on surface

int flash_time = 0;

String command;

long start = 0;

void setup()
{
  Serial.begin(9600);
  command = String();
  for(int pin = 3; pin <= 8; pin++){pinMode(pin, OUTPUT);}
  pinMode(led_pin, OUTPUT);
  pinMode(ultrasonic_echo, INPUT);
  pinMode(ultrasonic_trigger, OUTPUT);
  pinMode(master_enable, INPUT);
  delay(500);
  if(digitalRead(master_enable)) // only do the nice flashing if the Duino is disabled. otherwise, hurry up by not flashing!
  {
    for(int i = 0; i <= 10; i++)
    {
      digitalWrite(led_pin, HIGH);
      delay(50);
      digitalWrite(led_pin, LOW);
      delay(50);
    }
  }
  Serial.print("DUINO-READY\r\n"); // tell Pi the Duino is OK and ready to answer commands
  while(digitalRead(master_enable)){delay(20);} // wait until Pi sets "duino master enable" pin to "enable" (LOW)
}

void loop()
{
  start = millis();
  if(!digitalRead(master_enable))
  {
    if(disabled)
    {
      while(Serial.available() > 0){Serial.read();} // clear any old data
      pan.attach(pan_servo);
      pan.writeMicroseconds(pan_ms);
      tilt.attach(tilt_servo);
      tilt.writeMicroseconds(tilt_ms);
      flash_time = 0;
      disabled = true;
    }
    get_commands();
    step_left_motor();
    step_right_motor();
    if(flash_time > 25){digitalWrite(led_pin, !digitalRead(led_pin));flash_time = 0;}else{flash_time ++;} // flash board led
    delay(constrain((loop_pause - (millis() - start)), 0, loop_pause)); // run loop every $loop_pause milliseconds, accurately. calculate elapsed time since loop began and deduct from delay time
  }
  else
  {
    while(Serial.available() > 0){Serial.read();} // clear any data that's accumalating.
    if(!disabled)
    {
      pan.detach();
      tilt.detach();
      digitalWrite(led_pin, LOW);
      flash_time = 0;
      disabled = false;
    }
    freeze_motors();
    if(flash_time > 300){digitalWrite(led_pin, HIGH);delay(30);digitalWrite(led_pin, LOW);flash_time = 0;}else{flash_time ++;} // flash board led
    delay(constrain((loop_pause - (millis() - start)), 0, loop_pause)); // run loop every $loop_pause milliseconds, accurately. calculate elapsed time since loop began and deduct from $loop_pause
  }
}
