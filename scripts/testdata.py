"""Skickar påhittade mätvärden till mosquitto.

Vi använder den här när vi vill testa pipelinen utan att ha Pico:n inkopplad,
till exempel när vi ska ta skärmbilder på Grafana eller låta allt rulla länge
för att se att inget hänger sig.

OBS: det här är INTE riktig sensordata. Skärmbilder till redovisningen ska tas
med Pico:n inkopplad.

    uv run --with paho-mqtt scripts/testdata.py
    uv run --with paho-mqtt scripts/testdata.py --broker 192.168.1.141 --interval 1
"""

import argparse
import json
import math
import random
import time

import paho.mqtt.client as mqtt

TOPIC = "pico/serverroom/dht11"
DEVICE_ID = "pico-serverroom-sim"

TEMP_LIMIT = 27
HUMIDITY_LIMIT = 60


def get_status(temperature, humidity):
    if temperature > TEMP_LIMIT or humidity > HUMIDITY_LIMIT:
        return "ALARM"
    return "OK"


def main():
    parser = argparse.ArgumentParser(description="skickar testdata till mosquitto")
    parser.add_argument("--broker", default="localhost", help="ip till mosquitto")
    parser.add_argument("--interval", type=float, default=3, help="sekunder mellan mätvärden")
    parser.add_argument("--minutes", type=float, default=0, help="hur länge, 0 = tills man avbryter")
    args = parser.parse_args()

    client = mqtt.Client()
    client.connect(args.broker, 1883)
    print(f"Ansluten till {args.broker}, skickar till {TOPIC}")

    start = time.time()
    steg = 0

    while True:
        # temperaturen går långsamt upp och ner runt larmgränsen så att vi får
        # både OK och ALARM i grafen, precis som när serverrummet blir varmt
        temperature = round(25 + 3 * math.sin(steg / 40) + random.uniform(-0.4, 0.4))
        humidity = round(45 + 12 * math.sin(steg / 55) + random.uniform(-1, 1))
        status = get_status(temperature, humidity)

        data = {
            "device_id": DEVICE_ID,
            "temperature": temperature,
            "humidity": humidity,
            "status": status,
        }
        client.publish(TOPIC, json.dumps(data))
        print(f"sent: {data}")

        steg += 1
        if args.minutes and time.time() - start > args.minutes * 60:
            print("Klart.")
            break

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
