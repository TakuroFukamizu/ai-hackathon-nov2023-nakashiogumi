#include <arduino.h>
#include <WiFi.h>
#include <FastLED.h>
#include "wificonfig.h"

#define NUM_LEDS 121 // 35*3+8*2
#define PIN_LEDS 25

CRGB leds[NUM_LEDS];

int textsize = 3;
// uint8_t effectMode = 0; 
uint8_t effectMode = 4; 
/* 
0: black,
1: challenger1 speaking
2: challenger2 speaking
3: judge thinking
4: judge selected challenger1
5: judge selected challenger2
*/

uint8_t challenger1CircleIndex = 0; // 0..34
uint8_t challenger1BarIndex = 42; // 42..35
uint8_t judgeCircleIndex = 43; // 43..77
uint8_t challenger2BarIndex = 78; // 78..85
uint8_t challenger2CircleIndex = 86; // 86..120
uint8_t blinkToggle = 0;

void turnOffAll();
void ledTest();
void setIndexsToStart();
void challenger1WinStart();
void challenger1WinRun();

void setup() { 
    Serial.begin(115200);

    // Serial.print("WiFi connect");
    // WiFi.begin(WIFI_SSID, WIFI_PASS);
    // while (WiFi.status() != WL_CONNECTED){
    //     delay(500);
    //     Serial.print('.');
    // }
    // Serial.print("\n");
    // Serial.println(WiFi.localIP());

    FastLED.addLeds<NEOPIXEL, PIN_LEDS>(leds, NUM_LEDS); 
    Serial.println("led test");
    ledTest();

    Serial.println("boot ok");
    challenger1WinStart();
}
/*
LED Mapping
  0- 34(35): Challenger1 Circle
 35- 43( 8): Challenger1 Bar
 43- 77(35): Judge Circle
 78- 86( 8): Challenger2 Bar
 87-121(35): Challenger2 Circle
*/
void loop() {
    Serial.println("led test");
    // ledTest();
    
    switch(effectMode) {
        case 0: // turn off all
            turnOffAll();
            break;
        case 1: // challenger1 speaking
            break;
        case 2: // challenger2 speaking
            break;
        case 3: // judge thinking
            break;
        case 4: // judge selected challenger1
            challenger1WinRun();
            break;
        case 5: // judge selected challenger2
            break;

    }
    delay(30);
}

// --------

void turnOffAll() {
    for(int i=0;i<NUM_LEDS;i++) {
        leds[i] = CRGB::Black;
    }
    FastLED.show();
}

void ledTest() {
    turnOffAll();
    // Challenger1 Circle 
    for(int a=0;a<35;a++) {
        leds[a] = CRGB::Red; // current
    }
    FastLED.show(); 
    delay(500);
    // ----
    turnOffAll();
    // Challenger1 Bar
    for(int b=35;b<43;b++) {
        leds[b] = CRGB::White; // current
    }
    FastLED.show(); 
    delay(500);
    // ----
    turnOffAll();
    // Judge Circle
    for(int c=43;c<78;c++) {
        leds[c] = CRGB::Green; // current
    }
    FastLED.show(); 
    delay(500);
    // ----
    turnOffAll();
    // Challenger2 Bar
    for(int d=78;d<86;d++) {
        leds[d] = CRGB::White; // current
    }
    FastLED.show(); 
    delay(500);
    // ----
    turnOffAll();
    // Challenger1 Circle 
    for(int e=86;e<121;e++) {
        leds[e] = CRGB::Blue; // current
    }
    FastLED.show(); 
    delay(500);
    // ----
    turnOffAll();
}



void setIndexsToStart()
{
    challenger1CircleIndex = 0; // 0..34
    challenger1BarIndex = 42; // 42..35
    judgeCircleIndex = 43; // 43..77
    challenger2BarIndex = 78; // 78..85
    challenger2CircleIndex = 86; // 86..120
}

void challenger1WinStart()
{
    turnOffAll(); // clear all
    setIndexsToStart(); // clear all index
    blinkToggle = 0;
}
void challenger1WinRun() {
    // Judge Circle
    for(int c=43;c<78;c++) {
        if (blinkToggle==0) {
            leds[c] = CRGB::Green;
        } else {
            leds[c] = CRGB::Black;
        }
    }
    // Challenger1 Circle 
    for(int a=0;a<35;a++) {
        if (blinkToggle==0) {
            leds[a] = CRGB::Green;
        } else {
            leds[a] = CRGB::Black;
        }
    }
    blinkToggle++;
    if (blinkToggle>1) {
        blinkToggle = 0;
    }
    // ----
    // Challenger1 Bar
    for(int b=35;b<43;b++) {
        leds[b] = CRGB::Black; // clear all
    }
    leds[challenger1BarIndex] = CRGB::White;
    challenger1BarIndex--; // 42..35
    if (challenger1BarIndex<35) {
        challenger1BarIndex = 42;
    }
    FastLED.show();
    delay(100);
}