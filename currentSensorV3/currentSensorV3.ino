// CurrentSensorV3 - Robert J Scales 2021
// This code has been designed for the Arduino UNO (https://amzn.to/3cWtmLj) with this current sesnor (https://amzn.to/2NJbhYx).
// This code works in conjunction with a Python code I have written that looks at the serial output from the Arduino, which then saves saves those readings as a csv file.



#include <Wire.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219(0x45);


void setup(void) 
{
  Serial.begin(9600); // 115200
  while (!Serial) {
      // will pause Zero, Leonardo, etc until serial console opens
      delay(1);
  }

  uint32_t currentFrequency;
    
  // Serial.println("Code started");
  
  // Initialize the INA219.
  // By default the initialization will use the largest range (32V, 2A).  However
  // you can call a setCalibration function to change this range (see comments).
  if (! ina219.begin()) {
    Serial.println("Failed to find INA219 chip");
    while (1) { delay(10); }
  }
  // To use a slightly lower 32V, 1A range (higher precision on amps):
  //ina219.setCalibration_32V_1A();
  // Or to use a lower 16V, 400mA range (higher precision on volts and amps):
  //ina219.setCalibration_16V_400mA();

  Serial.println("Measuring voltage and current with INA219 ...");
}

bool label = true;

void loop(void) 
{
  float shuntvoltage = 0;
  float busvoltage = 0;
  float current_mA = 0;
  float loadvoltage = 0;
  float power_mW = 0;

  shuntvoltage = ina219.getShuntVoltage_mV();
  busvoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  power_mW = ina219.getPower_mW();
  loadvoltage = busvoltage + (shuntvoltage / 1000);

  //print out column headers
  while(label){ //runs once
        Serial.print("Bus Voltage (V):");
        Serial.print(",");
        Serial.print("Shunt Voltage (mV):");
        Serial.print(",");
        Serial.print("Load Voltage (V):");
        Serial.print(",");
        Serial.print("Current (mA):");
        Serial.print(",");
        Serial.println("Power (mW):");
        label=false;
  }

  // Display Data in CSV Format in Serial Monitor
  Serial.print(busvoltage);
  Serial.print(",");
  Serial.print(shuntvoltage);
  Serial.print(",");
  Serial.print(loadvoltage);
  Serial.print(",");
  Serial.print(current_mA);
  Serial.print(",");
  Serial.println(power_mW);

  
//  Serial.print("Bus Voltage:   "); Serial.print(busvoltage); Serial.println(" V");
//  Serial.print("Shunt Voltage: "); Serial.print(shuntvoltage); Serial.println(" mV");
//  Serial.print("Load Voltage:  "); Serial.print(loadvoltage); Serial.println(" V");
//  Serial.print("Current:       "); Serial.print(current_mA); Serial.println(" mA");
//  Serial.print("Power:         "); Serial.print(power_mW); Serial.println(" mW");
//  Serial.println("");

  delay(1000); //data collection frequency ~x milliseconds
}
