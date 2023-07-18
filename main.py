import json
import socket
import requests
import datetime
import time

ip_address = ''
port = 38899
url = 'https://api.spot-hinta.fi/Justnow'
off_hour = 0
on_hour = 7

while True:
    current_time = datetime.datetime.now().time()

    if current_time.minute == 2:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            price_with_tax = data['PriceWithTax']
            price_with_tax *= 100
            print(f"Price with tax: {price_with_tax}")

            # Determine the color based on the price range
            if price_with_tax < 7:
                command = {
                    'id': 1,
                    'method': 'setPilot',
                    'params': {
                        'r': 0,
                        'g': 255,
                        'b': 0,
                        'dimming': 100
                    }
                }
            elif 7 <= price_with_tax <= 15:
                command = {
                    'id': 1,
                    'method': 'setPilot',
                    'params': {
                        'r': 255,
                        'g': 255,
                        'b': 0,
                        'dimming': 100
                    }
                }
            else:
                command = {
                    'id': 1,
                    'method': 'setPilot',
                    'params': {
                        'r': 255,
                        'g': 0,
                        'b': 0,
                        'dimming': 100
                    }
                }

            if off_hour <= current_time.hour <= on_hour:
                command = {
                    'id': 1,
                    'method': 'setPilot',
                    'params': {
                        'state': 'false'
                    }
                }

            command_string = json.dumps(command)
            message = command_string.encode()

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(message, (ip_address, port))
            client_socket.close()
        else:
            print(f'Failed to fetch data. Status code: {response.status_code}')

    # Delay until the next target time
    next_hour = (datetime.datetime.now() + datetime.timedelta(hours=1)).replace(minute=2, second=0, microsecond=0)
    time.sleep((next_hour - datetime.datetime.now()).total_seconds())
