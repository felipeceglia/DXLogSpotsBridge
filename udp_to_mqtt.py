import asyncio
import socket
import re
import paho.mqtt.client as mqtt

IP = "0"  
UDP_PORT = 9888

MQTT_BROKER_HOST = "localhost"  # Change to your MQTT broker's host
MQTT_BROKER_PORT = 1883  # Default MQTT port
MQTT_TOPIC = "DXLOG"

async def post_spot(spot, mqtt_client):
    mqtt_client.publish(MQTT_TOPIC, spot)

async def read_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, UDP_PORT))

    mqtt_client = mqtt.Client()
    mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    mqtt_client.loop_start()

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode("utf-16-le")
            #print(f'{message}')

            x = re.search(r'.*\d+BANDMAP->(DX de .*$)', message)
            if x is not None:
                print(f'got UDP: {message}')
                mqtt_client.publish('DXLOG_SPOTS', x.group(1))

        except KeyboardInterrupt:
            print("Exiting...")
            break

    # Close the socket and disconnect MQTT client
    sock.close()
    mqtt_client.disconnect()
    mqtt_client.loop_stop()

if __name__ == '__main__':

    print(f"Listening for UDP messages on {IP}:{UDP_PORT}...")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_udp())
    loop.run_forever()
