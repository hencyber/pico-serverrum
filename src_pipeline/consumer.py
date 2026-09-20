import paho.mqtt.client as mqtt
import json
import os
from utils.connect_postgres import query_db

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
TOPIC = "pico/serverroom/dht11"


def create_table():
    query_db("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            time TIMESTAMPTZ NOT NULL,
            device_id TEXT,
            temperature DOUBLE PRECISION,
            humidity DOUBLE PRECISION,
            status TEXT
        )
    """)
    # timescaledb wants a hypertable to be able to handle timeseries data fast
    query_db("""
        SELECT create_hypertable('sensor_readings', 'time', if_not_exists => TRUE)
    """)


def on_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)

    device_id = data["device_id"]
    temperature = float(data["temperature"])
    humidity = float(data["humidity"])
    status = data["status"]

    query_db(
        """
        INSERT INTO sensor_readings
            (time, device_id, temperature, humidity, status)
        VALUES (NOW(), %s, %s, %s, %s)
""",
        (device_id, temperature, humidity, status),
    )

    print(f"saved: {device_id} {temperature}°C {humidity}% {status}")


def on_connect(client, userdata, flags, rc):
    # we subscribe here and not once at the start, because paho drops the
    # subscription when it reconnects. without this the consumer stays
    # connected but stops receiving anything
    print(f"Connected to mosquitto, listening on topic {TOPIC}")
    client.subscribe(TOPIC)


if __name__ == "__main__":
    create_table()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883)
    client.loop_forever()
