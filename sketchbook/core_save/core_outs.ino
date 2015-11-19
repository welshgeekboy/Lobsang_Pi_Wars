// motor control

void freeze_motors()
{
  digitalWrite(left_motor_enable, LOW);
  digitalWrite(right_motor_enable, LOW);
  left_motor_value = 0;
  right_motor_value = 0;
  left_motor_aim = 0;
  right_motor_aim = 0;
}

void step_left_motor()
{
  int pwm = 0;
  if(left_motor_aim != left_motor_value)
  {
    if(left_motor_aim > left_motor_value)
    {
      left_motor_value ++;
    }
    else if(left_motor_aim < left_motor_value)
    {
      left_motor_value --;
    }
    if(left_motor_value >= 0)
    {
      pwm = constrain(left_motor_value * 16, 0, 255);
      analogWrite(left_motor_enable, pwm);
      digitalWrite(left_motor_forward, HIGH);
      digitalWrite(left_motor_backward, LOW);
    }
    else
    {
      pwm = constrain(left_motor_value * -16, 0, 255);
      analogWrite(left_motor_enable, pwm);
      digitalWrite(left_motor_forward, LOW);
      digitalWrite(left_motor_backward, HIGH);
    }
  }
}

void step_right_motor()
{
  int pwm = 0;
  if(right_motor_aim != right_motor_value)
  {
    if(right_motor_aim > right_motor_value)
    {
      right_motor_value ++;
    }
    else if(right_motor_aim < right_motor_value)
    {
      right_motor_value --;
    }
    if(right_motor_value >= 0)
    {
      pwm = constrain(right_motor_value * 16, 0, 255);
      analogWrite(right_motor_enable, pwm);
      digitalWrite(right_motor_forward, HIGH);
      digitalWrite(right_motor_backward, LOW);
    }
    else
    {
      pwm = constrain(right_motor_value * -16, 0, 255);
      analogWrite(right_motor_enable, pwm);
      digitalWrite(right_motor_forward, LOW);
      digitalWrite(right_motor_backward, HIGH);
    }
  }
}

void set_left_motor(int spd)
{
  int pwm = 0;
  if(spd >= 0)
  {
    pwm = constrain(left_motor_value * 16, 0, 255);
    analogWrite(left_motor_enable, pwm);
    digitalWrite(left_motor_forward, HIGH);
    digitalWrite(left_motor_backward, LOW);
  }
  else
  {
    pwm = constrain(left_motor_value * -16, 0, 255);
    analogWrite(left_motor_enable, pwm);
    digitalWrite(left_motor_forward, LOW);
    digitalWrite(left_motor_backward, HIGH);
  }
}

void set_right_motor(int spd)
{
  int pwm = 0;
  if(spd >= 0)
  {
    pwm = constrain(right_motor_value * 16, 0, 255);
    analogWrite(right_motor_enable, pwm);
    digitalWrite(right_motor_forward, HIGH);
    digitalWrite(right_motor_backward, LOW);
  }
  else
  {
    pwm = constrain(right_motor_value * -16, 0, 255);
    analogWrite(right_motor_enable, pwm);
    digitalWrite(right_motor_forward, LOW);
    digitalWrite(right_motor_backward, HIGH);
  }
}

// sensors

float ultrasonic_distance()
{
  float cm = 0;
  long elapsed_us = 0;
  for(int i = 0; i < 5; i ++) // loop four times for mean averaging (= more accuracy but 3x slower)
  {
    digitalWrite(ultrasonic_trigger, LOW);
    delayMicroseconds(2);
    digitalWrite(ultrasonic_trigger, HIGH);
    delayMicroseconds(10);
    digitalWrite(ultrasonic_trigger, LOW);
    elapsed_us = pulseIn(ultrasonic_echo, HIGH);
    cm += elapsed_us / 58.77; // convert microseconds to centimetres and halve distance all in one go
  }
  cm /= 4; // finish mean averaging
  return cm;
}
