# Lobsang_Pi_Wars

This is all the code used on Lobsang, my Pi Wars 2015 competing robot.
My blog about the Pi Wars challenge is at www.letsmakerobots.com/blog/23676

Description of each file:
  Libraries:
    Lobsang.py- created by me to run everything Lobsang can do. Does not include logic though (as in for instance line following).
    Oled.py- created by me to control the OLED screen on the back of Lobsang that displays simple information.
    Padlock.py- created by me to act like a login in the terminal, can stop system access if wrong passkey given.
    There are other libraries that I use (eg. pygame) which are part of Python, not created by me.
  Challenge files:
    piwars_menu.py- runs a menu on the OLED for running the different challenge programs. Uses pygame to get user inputs.
    line_follower.py- follows a black line on a white background.
    proximity_alert.py- drives up to a wall as close as possible but does not touch.
    manual_control.py- allows a user to control the robot with W, A, S, D keys.
    drag_race.py- manual control for the straight line speed test- only slight turning is enabled.
  Other files:
    autorun.py- runs on Pi booting, checks if all testable aspects of the robot are online and if they are then runs piwars_menu.py, else gives a login prompt.
    boot.py- does the actual system checking.
    
