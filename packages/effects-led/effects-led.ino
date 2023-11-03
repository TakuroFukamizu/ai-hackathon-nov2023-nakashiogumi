#include <arduino.h>
#include <M5Unified.h>
#include <WiFi.h>
#include <FastLED.h>
#include "wificonfig.h"

#define NUM_LEDS 60

CRGB leds[NUM_LEDS];
int textsize = 3;

void setup() { 
    auto cfg = M5.config();
    // cfg.serial_baudrate = 115200;
    M5.begin(cfg);

    Serial.print("WiFi connect");
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED){
        delay(500);
        Serial.print('.');
    }
    Serial.print("\n");
    Serial.println(WiFi.localIP());

    FastLED.addLeds<NEOPIXEL, 6>(leds, NUM_LEDS); 

    textsize = M5.Displays(0).height() / 60;
    if (textsize == 0) { textsize = 1; }
    M5.Displays(0).setTextSize(textsize);
    M5.Displays(0).printf("Boot");
    Serial.println("boot ok");
}

void loop() {
    leds[0] = CRGB::White; FastLED.show(); delay(30);
    leds[0] = CRGB::Black; FastLED.show(); delay(30);
}
