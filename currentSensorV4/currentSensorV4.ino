// CurrentSensorV4 - Robert J Scales 2021
// This code has been designed for the Arduino UNO (https://amzn.to/3cWtmLj) with this current sesnor (https://amzn.to/2NJbhYx).
// This code works in conjunction with a Python code I have written that looks at the serial output from the Arduino, which then saves saves those readings as a csv file.



#include <Wire.h>
#include <Adafruit_INA219.h>
#include <Wire.h>
#include <Adafruit_I2CDevice.h>
#include <Adafruit_I2CRegister.h>
#include "Adafruit_MCP9600.h"

#define I2C_ADDRESS (0x67)
Adafruit_MCP9600 mcp;
Adafruit_INA219 ina219(0x45);

void setup(void) 
{
  Serial.begin(115200); // 115200 or 9600
  while (!Serial) {
      // will pause Zero, Leonardo, etc until serial console opens
      delay(1);
  }

//  Serial.println("MCP9600 HW test");

  /* Initialise the driver with I2C_ADDRESS and the default I2C bus. */
  if (! mcp.begin(I2C_ADDRESS)) {
      Serial.println("Sensor not found. Check wiring!");
      while (1);
  }

//  Serial.println("Found MCP9600!");
  mcp.setADCresolution(MCP9600_ADCRESOLUTION_18);
  mcp.setThermocoupleType(MCP9600_TYPE_K);
  mcp.setFilterCoefficient(3);

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
  ina219.setCalibration_32V_1A(); // Uncommented this.
  // Or to use a lower 16V, 400mA range (higher precision on volts and amps):
  //ina219.setCalibration_16V_400mA();

  // Serial.println("Measuring voltage and current with INA219 ...");
}

//bool label = false;

void loop(void) 
{
  float shuntvoltage = 0;
  float busvoltage = 0;
  float current_mA = 0;
  float loadvoltage = 0;
  float power_mW = 0;
  float probe_temperature = 100;
  float device_temperature = 99;
  // float ADC = 0;

  shuntvoltage = ina219.getShuntVoltage_mV();
  busvoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  power_mW = ina219.getPower_mW();
  loadvoltage = busvoltage + (shuntvoltage / 1000);
  probe_temperature = mcp.readThermocouple();
  device_temperature = mcp.readAmbient();
//  ADC = mcp.readADC() * 2;

  // Display Data in CSV Format in Serial Monitor
//  Serial.print(busvoltage); // Bus Voltage (V) 
//  Serial.print(","); Serial.print(shuntvoltage); // Shunt Voltage (mV)
//  Serial.print(","); Serial.print(power_mW); // Power (mW)
//  Serial.print(","); 
  Serial.print(loadvoltage); // Load Voltage (V)
  Serial.print(","); Serial.print(current_mA); // Current (mA)
  Serial.print(","); Serial.print(probe_temperature); // Temperature of probe i.e. hot junction (C)
  Serial.print(","); Serial.println(device_temperature); // Temperature of device i.e. cold junction (C)
//  Serial.print(","); Serial.println(ADC); // ADC value (uV)

  delay(100); // Changed from 1000 to 100 . Data collection frequency ~x milliseconds
}
