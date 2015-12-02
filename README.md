# Lobsang's Pi Wars code, plus the robot's general purpose libraries.

<p>This is all the code used on Lobsang, my Pi Wars 2015 competing robot.</p>
<p>My blog about the Pi Wars challenge is at <a href="http:www.letsmakerobots.com/blog/23676">LetsMakeRobots.com</a> where you will find details of the build and code development.</p>

<p>Description of each file:
	<ul><h5>Libraries:</h5>
		<li>Lobsang.py- created by me to run everything Lobsang can do. Does not include logic though (as in for instance line following).</li>
		<li>Oled.py- created by me to control the OLED screen on the back of Lobsang that displays simple information.</li>
		<li>Padlock.py- created by me to act like a login in the terminal, can stop system access if wrong passkey given.</li>
		<li>There are other libraries that I use (eg. pygame) which are part of Python, not created by me.</li>
	</ul>
	<ul><h5>Challenge files:</h5>
		<li>piwars_menu.py- runs a menu on the OLED for running the different challenge programs. Uses pygame to get user inputs.</li>
		<li>line_follower.py- follows a black line on a white background.</li>
		<li>proximity_alert.py- drives up to a wall as close as possible but does not touch.</li>
		<li>manual_control.py- allows a user to control the robot with W, A, S, D keys.</li>
		<li>drag_race.py- manual control for the straight line speed test- only slight turning is enabled.</li>
	</ul>
	<ul><h5>Other files:</h5>
		<li>autorun.py- runs on Pi booting, checks if all testable aspects of the robot are online and if they are then runs piwars_menu.py, else gives a login prompt.</li>
		<li>boot.py- does the actual system checking.</li>
    	</ul>

