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
  Serial.println("S");
  // loop through all the cd4015 I/O, or known as every kaki
  for (int y = 0; y < 8; ++y){//for each breadboard jack
    digitalWrite(a, HIGH && (y & B00000001)); //still loop
    digitalWrite(b, HIGH && (y & B00000010));
    digitalWrite(c, HIGH && (y & B00000100));
    for (int x = 0; x < 2; ++x){//for each module
      int data = analogRead(pin[x]);
        if(data < 700){
          Serial.print(x);
          Serial.print(";");
          Serial.print(y);
          Serial.print(";");
          Serial.println(data);
          }
      }
    }
  Serial.println("T");

}
