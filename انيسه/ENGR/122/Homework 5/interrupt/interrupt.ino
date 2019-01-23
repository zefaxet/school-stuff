int led = 13;

int blue = 7;
int green = 10;
int red = 12;

int state = 0;
int period = 0;

void setup() {

  pinMode(led,OUTPUT);
  pinMode(blue,OUTPUT);
  pinMode(green,OUTPUT);
  pinMode(red,OUTPUT);

  Serial.begin(9600);
  attachInterrupt(0,whisker,CHANGE);

}

void loop() {

  while (1) {
    //increases to 3140 by increments of 157
    period += 157;
    //divice that number by 1000 to get a number less than or equal to pi
    float ratio = (period % 3140) / float(1000);
    //make red led blink
    state = !state;
    //delay is a function of the current fraction of pi
    delay(45 * (sin(ratio) + 1));
    digitalWrite(led, state);
  }

}

void whisker() {

  digitalWrite(blue, random(0,2));
  digitalWrite(red, random(0,2));
  digitalWrite(green, random(0,2));
  
}

