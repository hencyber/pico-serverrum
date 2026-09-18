# This is the version we run in the wokwi simulation.
# Wokwi only has a DHT22 and no mosquitto broker, so here we just read the
# sensor and show the status with the led. The real code is in src_pico/main.py
from dht import DHT22
from machine import Pin
import time

time.sleep(.5)

sensor = DHT22(Pin(16))
status_led = Pin(15, Pin.OUT)

TEMP_LIMIT = 27
HUMIDITY_LIMIT = 60
SLEEP_TIME = 3


def get_status(temperature, humidity):
    if temperature > TEMP_LIMIT or humidity > HUMIDITY_LIMIT:
        return "ALARM"
    return "OK"


def show_status(status, seconds):
    # the led shines when everything is ok and blinks when there is an alarm
    if status == "OK":
        status_led.value(1)
        time.sleep(seconds)
    else:
        for _ in range(int(seconds * 4)):
            status_led.toggle()
            time.sleep(.25)
        status_led.value(0)


while True:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()

    status = get_status(temperature, humidity)

    print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Status: {status}")
    show_status(status, SLEEP_TIME)
