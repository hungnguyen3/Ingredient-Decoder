# Ingredients Decoder - CPEN 391

## Separate repository for hardware acceleration code:

https://github.com/nathan-n-poon/beep-boop

## Repo Contents:

- app_backend: backend API
- app_frontend: frontend of the Android app
- DE1_C_code: C code controlling the DE1-SoC board
- DE1_Quartus: contains the Quartus project to be loaded on DE1-SoC
- RPI: Python code controling the Raspberry Pi, touchscreen, camera, and sonar sensor

## Project Description:

<img src = "z_images/components.PNG" width = "450">

Our project is called Ingredient Decoder. It combines a physical device with a mobile app, to together provide a solution for shoppers wanting to know more about the ingredients inside the things they buy.

The physical device, called the Scanning Platform, consists of scanning devices as well as a touchscreen. It allows store customers to scan the items they wish to buy, and then view information regarding the items. It has been optimized for this role through custom FPGA hardware on the DE1.

The mobile app has similar scanning and analysis services, and also provides account management capabilities

## Component Descriptions:

### Altera DE1-SoC:

- Image cropping acceleration
- Sonar sensor distance HEX display
- Controlling the RFS board in C code
- Transceive data to and from a Raspberry Pi using RS232 serial connection

### Altera RFS board:

- Bluetooth login using HC-05 chip
- Sending Twilio SMS using ESP-WROOM-02 chip

### Raspberry Pi:

- Control the camera, the sonar sensor, and the touchscreen app
- Transceive data of the sonar sensor and images to and from DE1-SoC

### Android app:

- Scanning and analyzing items' ingredients
- account management capabilities
