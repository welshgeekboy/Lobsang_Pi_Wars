boolean r = false;
String iput;
int flash = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  iput = String();
}

void loop()
{
  while(Serial.available() > 0)
  {
    if(r == false){delay(50);iput = "";}
    iput += char(Serial.read());
    r = true;
  }
  if(iput == "HIGH")
  {
    digitalWrite(13, HIGH);
  }
  else if(iput == "LOW")
  {
    digitalWrite(13, LOW);
  }
  if(r == true)
  {
    Serial.print("Duino recieved data: " + iput + " and charAt(1) = ");
    r = false;
    flash = int(iput.charAt(1));
    Serial.print(flash);
    Serial.print("\r");
    /*flash = iput.indexOf("1");
    while(flash >= 0)
    {
      digitalWrite(13, HIGH);
      delay(200);
      digitalWrite(13, LOW);
      delay(200);
      flash --;
    }
    delay(300);
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(3, LOW);*/
  }
  delay(500);
}

