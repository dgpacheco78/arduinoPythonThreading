#include <Servo.h>
#include <Ticker.h>
#include <DHT.h>
#include <DHT_U.h>
#include <LiquidCrystal_I2C.h>

DHT dht(2, DHT11);
String cadenaJSon = "";
LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo servoM;

void leerDHT(){
  float hume = dht.readHumidity();        //humedad en porcentaje
  float temC = dht.readTemperature();     //grados centígrados
  float temF = dht.readTemperature(true); //grados Fahrenheit

  cadenaJSon = "{\"hume\":" + String(hume) + ", \"temC\":" + String(temC) + ", \"temF\":" + String(temF) + "}";

  Serial.println(cadenaJSon);
  lcd.setCursor(0, 1);                                    //mensaje de estado "listo" del sistema
  //lcd.print(String(hume) + " " + String(temC) + " " + String(temF));
}

Ticker tickerLeerDHT(leerDHT, 500);

void setup() {
  dht.begin();
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Secadora");
  tickerLeerDHT.start();
  servoM.attach(6);
}

void loop() {
  tickerLeerDHT.update();
  if(Serial.available() > 0 ){
      String dato = "";
      dato = Serial.readString();
      delay(100);
      dato.trim();
      int servInt = dato.toInt();
      servoM.write(servInt);
      lcd.print("" + servInt);     
      delay(100);
  }
}
