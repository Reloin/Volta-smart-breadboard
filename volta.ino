const int resistor = 2000;   //the fixed resistor used
const int offset = 0; //Eliminate inaccuracy

const char row[] = "abcdefgh";
const int pin[] = {A0, A1, A2, A3, A4, A5};

const int a = 2; //3 pin to rule them all
const int b = 3;
const int c = 4;

void setup() {
  
pinMode(10, INPUT);
pinMode(a, OUTPUT);
pinMode(b, OUTPUT);
pinMode(c, OUTPUT);

Serial.begin(9600);

}

void loop() {
  // loop through all the cd4015 I/O, or known as every kaki
  for (int i = 0; i < 8; ++i){//for each breadboard jack
    digitalWrite(a, HIGH && (i & B00000001)); //still loop
    digitalWrite(b, HIGH && (i & B00000010));
    digitalWrite(c, HIGH && (i & B00000100));
    
    for (int x = 0; x < 6; ++x){//for each module
      int data = analogRead(pin[x]);
      show(x, i);//display which pin is currently reading
      Serial.println(" "); //easier to read
      Serial.write(data);
      Serial.println("\n");
    }
    
  }

}


void show (int group, int pin) {
  //see if the received data is from left or right
  //for left hand side
  if (pin < 4) {
    switch (group) {
      case 0: Serial.write("1");
              break;
      case 1: Serial.write("1");
              break;
      case 2: Serial.write("3");
              break;
      case 3: Serial.write("3");
              break;
      case 4: Serial.write("5");
              break;
      case 5: Serial.write("5");
              break;        
    }
    if(group & 1) pin += 4;// to shift right hand side group to corresponding location
 }
 //for right hand side
 else {
    switch (group) {
      case 0: Serial.write("2");
              break;
      case 1: Serial.write("2");
              break;
      case 2: Serial.write("4");
              break;
      case 3: Serial.write("4");
              break;
      case 4: Serial.write("6");
              break;
      case 5: Serial.write("6");
              break;        
    }
    if(!(group & 1)) pin -= 4;//shift left hand side to corresponding location
 }
    
   Serial.write(row[pin]);
 }
