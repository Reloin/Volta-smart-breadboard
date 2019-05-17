const int resistor = 2000;  //the fixed resistor used
const int offset = 0; //Eliminate inaccuracy

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
  // loop through all the cd4015 I/O
  for (int i = 0; i < 8; ++i){
    digitalWrite(a, HIGH && (i & B00000001)); //still loop
    digitalWrite(b, HIGH && (i & B00000010));
    digitalWrite(c, HIGH && (i & B00000100));
    
    Serial.print("pin ");
    Serial.print(i);
    Serial.print(" = ");
    Serial.println(reading(A0)); // refer to the function
    delay(500);
    }


}

int reading(int pin){
  double data = analogRead(pin);
  double vout = 5*data/1023;
  int r =  resistor * vout /(5-vout);
  if(data > 1020){
    r = 0;
    }else{
      r -= offset;
      }
  return r;
  }
