
/*
solo uno scheletro per un codice futuro: scrivo al raspberry(collegato con la usb), lui legge, fa qualcosa, e
leggo il carattere che mi ha mandato(idealmente lui fa una foto e mi scrive il carattere che ha letto nella foto)
*/
void setup() {
  Serial.begin(9600);
}

void loop() {
  delay(100);
  //Serial.println("letter");
  while (Serial.available() == 0);
  
  if(Serial.available()>0){
    String letto= Serial.readStringUntil('\n');
    Serial.print(letto[0]);
  }

}
