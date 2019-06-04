const int resistor = 2000;   //the fixed resistor used

const char row[] = "ABCDEFGH";
const int pin[] = {A0, A1, A2, A3, A4, A5};

const int columnNum = 1;

const int a = 2; //3 pin to rule them all
const int b = 3;
const int c = 4;

void setup() {
  
  for(int i = 0; i < columnNum; ++i){
    pinMode(pin[i], INPUT);

  }

pinMode(a, OUTPUT);
pinMode(b, OUTPUT);
pinMode(c, OUTPUT);

Serial.begin(9600);

}

void loop() {
  // loop through all the cd4015 I/O, or known as every kaki
  for (int i = 0; i < 8; ++i){//for each breadboard jack
        //looping horizontally from left to right
    digitalWrite(a, HIGH && (i & B00000001)); //still loop
    digitalWrite(b, HIGH && (i & B00000010));
    digitalWrite(c, HIGH && (i & B00000100));
    
    for (int x = 0; x < columnNum; ++x){//for each module
      int data = analogRead(pin[x]);
      show(x, i);//display which pin is currently reading
      Serial.print(" "); //easier to read
      if(data > 1020){
        data = 0;
       }
      Serial.print(data);
      Serial.print("\n");
    }
    
  }
  delay(2000);

}


void show (int column, int pin) {
  //see if the received data is from left or right
  //for left hand side
  Serial.print(column + 1);
  Serial.print(row[pin]);
  
    
}
