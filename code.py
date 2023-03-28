import time

import board
import digitalio
import rotaryio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse


# Wired digial pins on board
keypress_pins = [board.D0, board.D7, board.D8, board.D9, board.D10]
# Key objects
key_pin_array = []
time.sleep(1)

# Rotary Encoder
encoder = rotaryio.IncrementalEncoder(board.D2, board.D1)
last_position = 0
encoder_persona = "volume"

# Human Interface Devices
consumer_control = ConsumerControl(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
mouse = Mouse(usb_hid.devices)

# Create Key objects
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)

led = digitalio.DigitalInOut(board.LED_INVERTED)
led.direction = digitalio.Direction.OUTPUT

print("Ready")

def run(app):
    print(app)
    keyboard.send(Keycode.WINDOWS, Keycode.R)
    time.sleep(0.4)
    keyboard_layout.write(app)
    time.sleep(0.1)
    keyboard.send(Keycode.ENTER)
    time.sleep(0.1)

# AutoRunner for Valheim
runThenWalk = False
def runThenWalk():
    while runThenWalk == True: 
        keyboard.press(Keycode.LEFT_SHIFT, Keycode.W)
        time.sleep(10)
        keyboard.release(Keycode.LEFT_SHIFT, Keycode.W)
        time.sleep(0.1)
        keyboard.press(Keycode.W)
        time.sleep(10)
        keyboard.release(Keycode.W)
        time.sleep(0.1)

while True:
    # Check configured digial pins
    for key_pin in key_pin_array:
        if not key_pin.value:
            i = key_pin_array.index(key_pin)

            while not key_pin.value:
                pass  # Wait for it to be ungrounded!

            if i == 0 :
              if encoder_persona == "volume" :
                encoder_persona = "scroll"
                print("Encoder persona: ", encoder_persona)
              elif encoder_persona == "scroll" :
                encoder_persona = "volume"
                print("Encoder persona: ", encoder_persona)

            if i == 1 :
              print("Play/Pause")
              consumer_control.send(ConsumerControlCode.PLAY_PAUSE)
              time.sleep(0.1)

            if i == 2 :
              print("Text extractor")
              keyboard.send(Keycode.WINDOWS, Keycode.LEFT_SHIFT, Keycode.T)
              time.sleep(0.1)
            
            if i == 3 :
              print("Open Firefox")
              run("firefox.exe")

            if i == 4 :
              print("Valheim Run then Walk loop")
              if runThenWalk == True :
                print("Stop running")
                runThenWalk = False
              if runThenWalk == False :
                print("Start running")
                runThenWalk = True

        # Encoder tracker
        position = encoder.position
        if last_position is None or position != last_position:
            if encoder_persona == "volume" :
                if position > last_position :
                    print("Volume up")
                    consumer_control.press(ConsumerControlCode.VOLUME_INCREMENT)
                    time.sleep(0.1)
                    consumer_control.release()
                if position < last_position :
                    print("Volume down")
                    consumer_control.press(ConsumerControlCode.VOLUME_DECREMENT)
                    time.sleep(0.1)
                    consumer_control.release()
            elif encoder_persona == "scroll" :
                if position > last_position :
                    print("Scroll up")
                    mouse.move(wheel=-1)
                if position < last_position :
                    print("Scroll down")
                    mouse.move(wheel=1)
        last_position = position

    time.sleep(0.01)
