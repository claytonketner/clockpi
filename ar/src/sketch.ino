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
int start_byte = int('s');
int end_byte = int('e');
int reset_byte = int('r');
int ping_byte = int('p');
int led_pin = 13;

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
    Serial.write('p');
}

void loop() {
    run_serial();
    write_display();
}

bool clean_serial() {
    // Empty serial until we find the start byte. Needing to clean serial
    // is a problem, so the LED will flash if cleaning is happening.
    // Returns true iff start byte was received
    bool led_state = false;
    int last_read = NULL;
    while (Serial.available() > 0 &&
           last_read != start_byte &&
           last_read != reset_byte) {
        last_read = Serial.read();
        digitalWrite(led_pin, led_state = !led_state);
        delay(100);
    }
    digitalWrite(led_pin, 0);

    if (last_read == reset_byte) {
        static_clear();
        initialize_displays(0);
        for (int array=0; array<num_arrays; array++) {
            for (int chip=0; chip<num_chips_per_array; chip++) {
                for (int row=0; row<8; row++) {
                    next_display[array][chip][row] = 0;
                }
            }
        }
    } else if (last_read == start_byte) {
        return true;
    } else if (last_read == ping_byte) {
        Serial.write('p');
    }
    return false;
}

void run_serial() {
    if (Serial.available() > 0) {
        if (!clean_serial()) { return; }
        int byte_index = 0;
        bool led_indicator = false;
        while (byte_index < (num_leds / 8)) {
            while (Serial.available() == 0) {
                digitalWrite(led_pin, led_indicator = !led_indicator);
                delay(500);
            }
            int next_byte = Serial.read();
            if (next_byte == ping_byte) {
                Serial.write('p');
            } else {
                next_display[int(byte_index / (8*num_chips_per_array))]
                            [int(byte_index / 8) % num_chips_per_array]
                            [byte_index % 8] = next_byte;
                byte_index++;
            }
        }
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

void run_test() {
    for (int col=0; col<8*num_chips_per_array; col++) {
        for (int array=0; array<num_arrays; array++) {
            lc[array].setColumn(int(col/8)%8, 7-(col%8), B11111111);
        }
    }
    static_clear();
    initialize_displays(0);
}

void static_clear() {
    // As items (rows/columns) get cleared, they get "removed" by shifting 
    // everything in the list over by one. We then ignore the n last
    // items in avail_*, where n is the value in num_avail_*
    int num_avail_chips = num_chips_per_array;
    int avail_chips[num_chips_per_array];
    int num_avail_rows[num_chips_per_array];
    int avail_rows[num_chips_per_array][8];
    int num_avail_pixels[num_chips_per_array][8];
    int avail_pixels[num_chips_per_array][8][8];
    for (int chip=0; chip<num_chips_per_array; chip++) {
        avail_chips[chip] = chip;
        num_avail_rows[chip] = 8;
        for (int row=0; row<8; row++) {
            avail_rows[chip][row] = row;
            num_avail_pixels[chip][row] = 8;
            for (int col=0; col<8; col++) {
                avail_pixels[chip][row][col] = col;
            }
        }
    }
    // Start clearing
    bool still_clearing = true;
    while (still_clearing) {
        still_clearing = false;
        int chip_index = random(num_avail_chips);
        int chip = avail_chips[chip_index];
        int row_index = random(num_avail_rows[chip]);
        int row = avail_rows[chip][row_index];
        int col_index = random(num_avail_pixels[chip][row]);
        int col = avail_pixels[chip][row][col_index];
        // Shift columns
        for (int ii=col_index; ii<num_avail_pixels[chip][row]; ii++) {
            avail_pixels[chip][row][ii] = avail_pixels[chip][row][ii+1];
        }
        num_avail_pixels[chip][row]--;
        // Shift rows (if the row has been cleared)
        if (num_avail_pixels[chip][row] == 0) {
            for (int ii=row_index; ii<num_avail_rows[chip]-1; ii++) {
                avail_rows[chip][ii] = avail_rows[chip][ii+1];
            }
            num_avail_rows[chip]--;
        }
        // Shift chips (if the chip has been cleared)
        if (num_avail_rows[chip] == 0) {
            for (int ii=chip_index; ii<num_avail_chips-1; ii++) {
                avail_chips[ii] = avail_chips[ii+1];
            }
            num_avail_chips--;
        }
        for (int array=0; array<num_arrays; array++) {
            lc[array].setLed(chip, row, col, false);
        }
        for (int chip=0; chip<num_chips_per_array; chip++) {
            if (num_avail_rows[chip] > 0) {
                still_clearing = true;
            }
        }
    }
}
