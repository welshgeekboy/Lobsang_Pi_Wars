void get_commands()
{
  if(Serial.available() > 0)
  {
    boolean serial_error = false;
    int thousands = 0;
    int hundreds = 0;
    int tens = 0;
    int units = 0;
    int command_length = 0;
    command = "";
TOO_SHORT://go here to read any extra data that may have accumulated, in case new command has not been read fully
    delay(15);
    while(Serial.available() > 0)
    {
      command += char(Serial.read());
    }
NEW_COMMAND: // if $command is more than one command in the same string eg "TS1200LMS29" then cycle through each command by going back to here
    if(command.startsWith("OK?")) // Pi poked the Duino to see if it's functioning properly
    {
      Serial.print("DUINO-OK\r\n"); // send an 'OK' reply through serial
      command_length = 3;
    }
    else if(command.startsWith("LMR") && command.length() > 4) // LMR == Left Motor 'Stepped' Ramped' to value specified from previous value
    {
      if(command.length() > 4)
      {
        tens = int(command.charAt(3)) - 48; // minus 48, as ASCII number values are N+48
        units = int(command.charAt(4)) - 48;
        left_motor_aim = constrain(tens * 10 + units - 16, -16, 16);
        command_length = 5;
      }
      else
      {
        goto TOO_SHORT;
      }
    }
    else if(command.startsWith("RMR") && command.length() > 4) // RMR == 'Right Motor Ramped' to value specified from previous value
    {
      if(command.length() > 4)
      {
        tens = int(command.charAt(3)) - 48;
        units = int(command.charAt(4)) - 48;
        right_motor_aim = constrain(tens * 10 + units - 16, -16, 16);
        command_length = 5;
      }
      else
      {
        goto TOO_SHORT;
      }
    }
    else if(command.startsWith("BMS") && command.length() > 4) // BMR == 'Both Motors Ramped' to value specified from previous value
    {
      if(command.length() > 4)
      {
        tens = int(command.charAt(3)) - 48;
        units = int(command.charAt(4)) - 48;
        left_motor_aim = constrain(tens * 10 + units - 16, -16, 16);
        right_motor_aim = left_motor_aim;
        command_length = 5;
      }
      else
      {
        goto TOO_SHORT;
      }
    }
    else if(command.startsWith("LMI") && command.length() > 4) // LMI == 'Left Motor Instantly' set to value specified
    {
      if(command.length() > 4)
      {
        tens = int(command.charAt(3)) - 48; // minus 48, as ASCII number values are N+48
        units = int(command.charAt(4)) - 48;
        left_motor_aim = constrain(tens * 10 + units - 16, -16, 16);
        left_motor_value = left_motor_aim;
        command_length = 5;
      }
      else
      {
        goto TOO_SHORT;
      }
    }
    else if(command.startsWith("RMI") && command.length() > 4) // RMI == 'Right Motor Instantly' set to value specified
    {
      if(command.length() > 4)
      {
        tens = int(command.charAt(3)) - 48;
        units = int(command.charAt(4)) - 48;
        right_motor_value = constrain(tens * 10 + units - 16, -16, 16);
        command_length = 5;
      }
      else
      {
        goto TOO_SHORT;
      }
    }
    else if(command.startsWith("BMI") && command.length() > 4) // BMI == 'Both Motors Instantly' set to value specified
    {
      if(command.length() > 4)
      {
        tens = int(command.charAt(3)) - 48;
        units = int(command.charAt(4)) - 48;
        left_motor_value = constrain(tens * 10 + units - 16, -16, 16);
        right_motor_value = left_motor_value;
        command_length = 5;
      }
      else
      {
        goto TOO_SHORT;
      }
    }
    else if(command.startsWith("PS") && command.length() > 5) // PS == set 'Pan Servo' to between 1000 and 2000 ms pulse
    {
      if(command.length() > 5)
      {
        thousands = int(command.charAt(2)) - 48;
        hundreds = int(command.charAt(3)) - 48;
        tens = int(command.charAt(4)) - 48;
        units = int(command.charAt(5)) - 48;
        pan_ms = constrain(thousands * 1000 + hundreds * 100 + tens * 10 + units, 1000, 2000);
        pan.writeMicroseconds(pan_ms);
        command_length = 6;
      }
      else
      {
        goto TOO_SHORT;
      }
    }
    else if(command.startsWith("TS") && command.length() > 5) // TS == set 'Tilt Servo' to between 1000 and 2000 ms pulse
    {
      if(command.length() > 5)
      {
        thousands = int(command.charAt(2)) - 48;
        hundreds = int(command.charAt(3)) - 48;
        tens = int(command.charAt(4)) - 48;
        units = int(command.charAt(5)) - 48;
        tilt_ms = constrain(thousands * 1000 + hundreds * 100 + tens * 10 + units, 1000, 2000);
        tilt.writeMicroseconds(tilt_ms);
        command_length = 6;
      }
      else
      {
        goto TOO_SHORT;
      }
    }
    else if(command.startsWith("US?")) // US == Pi asked for 'Ultrasonic Sensor' proximity data (returns value in cm)
    {
      distance_cm = ultrasonic_distance();
      Serial.print("US");
      Serial.print(distance_cm);
      Serial.print("\r\n");
      command_length = 2;
    }
    else if(command.startsWith("BV?")) // BV == Pi asked for 'Battery Voltage' to see if voltage is still okay
    {
      battery_voltage = analogRead(A0); // TODO: calculate proper voltage
      Serial.print("BV");
      Serial.print(battery_voltage);
      Serial.print("\r\n");
      command_length = 3;
    }
    else // error handling. command is none of the above. tell the Pi there's a problem
    {
      Serial.print("NO <"+ command +">\r\n");
      while(Serial.available() > 0){Serial.read();}// flush out any old data
      serial_error = true;
      command = "";
      command_length = 0;
    }
    if(command.length() > command_length && !serial_error)
    {
      command = command.substring(command_length); // remove old command and run this function again from NEW_COMMAND
      command_length = 0;
      goto NEW_COMMAND;
    }
  }
}
