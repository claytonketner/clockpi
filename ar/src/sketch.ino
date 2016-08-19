#include "LedControl.h"
#include "binary.h"

/*
LedControl args:
    1st pin arg is connected to the DataIn 
    2nd pin arg is connected to the CLK - PWM
    3rd pin arg is connected to LOAD/CS - PWM
*/
const int num_arrays = 2;
const int num_chips_per_array = 5;
const int num_leds = 8 * 8 * 2 * 5;
LedControl lc[2] = {
    LedControl(9,11,10,num_chips_per_array),
    LedControl(7,5,6,num_chips_per_array),
};
byte next_display[num_arrays][num_chips_per_array][8];
int ping_byte = int('p');
int led_pin = 13;
int serial_timeout = 1000;  // #1
int chunk_size = 60;  // #2

void initialize_displays(int brightness) {
    // Brightness 0-15
    for (int array=0; array<num_arrays; array++) {
        for (int ii=0; ii<lc[array].getDeviceCount(); ii++) {
            lc[array].shutdown(ii, true);
            lc[array].shutdown(ii, false);
            lc[array].setIntensity(ii, brightness);
            lc[array].clearDisplay(ii);
        }
    }
}

void setup() {
    Serial.begin(9600);
    pinMode(led_pin, OUTPUT);
    initialize_displays(0);
    randomSeed(analogRead(0));
    for (int array=0; array<num_arrays; array++) {
        for (int matrix=0; matrix<lc[array].getDeviceCount(); matrix++) {
            for (int row=0; row<8; row++) {
                next_display[array][matrix][row] = 0;
            }
        }
    }
    Serial.write(ping_byte); // Ready for operation
}

void loop() {
    run_serial();
    write_display();
}

bool wait_for_serial() {
    // Returns false if waiting timed out
    bool led_state = false;
    unsigned long start_time = millis();
    unsigned long last_led_update = start_time;
    while (Serial.available() == 0) {
        unsigned long now = millis();
        if (now - start_time > serial_timeout) {
            return false;
        }
        // Flash LED while we wait
        if (now - last_led_update > 500) {
            digitalWrite(led_pin, led_state = !led_state);
            last_led_update = now;
        }
    }
    digitalWrite(led_pin, 0);
    return true;
}

void run_serial() {
    if (Serial.available() > 0) {
        int byte_index = 0;
        while (byte_index < (num_leds / 8)) {
            if (!wait_for_serial()) { return; }
            int next_byte = Serial.read();
            next_display[int(byte_index / (8*num_chips_per_array))]
                        [int(byte_index / 8) % num_chips_per_array]
                        [byte_index % 8] = next_byte;
            byte_index++;
            if (byte_index % chunk_size == 0) {
                Serial.write(ping_byte);
            }
        }
        Serial.write(ping_byte);
    }
}

void write_display() {
    for (int array=0; array<num_arrays; array++) {
        for (int chip=0; chip<num_chips_per_array; chip++) {
            for (int row=0; row<8; row++) {
                lc[array].setRow(chip, row, next_display[array][chip][row]);
            }
        }
    }
}
