# This is the version we run in the wokwi simulation.
# Wokwi only has a DHT22 and no mosquitto broker, so here we just read the
# sensor and show the status with the LEDs. The real code is in src_pico/main.py
from dht import DHT22
from machine import Pin
import time

time.sleep(.5)

sensor = DHT22(Pin(16))
green_led = Pin(15, Pin.OUT)
red_led = Pin(14, Pin.OUT)

TEMP_LIMIT = 27
HUMIDITY_LIMIT = 60
SLEEP_TIME = 3


def get_status(temperature, humidity):
    if temperature > TEMP_LIMIT or humidity > HUMIDITY_LIMIT:
        return "ALARM"
    return "OK"


def show_status(status):
    green_led.value(1 if status == "OK" else 0)
    red_led.value(1 if status == "ALARM" else 0)


while True:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()

    status = get_status(temperature, humidity)
    show_status(status)

    print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Status: {status}")
    time.sleep(SLEEP_TIME)
