from os import environ
import logging
import requests
import binascii
from datetime import datetime
import json
import re

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")


cars = []
total = 0


def unix_timestamp_to_datetime(timestamp):
    # Convert the Unix timestamp to a datetime object
    dt = datetime.utcfromtimestamp(timestamp)

    # Format the datetime object to a readable string
    readable_time = dt.strftime('%Y-%m-%d %H:%M:%S')

    return readable_time


def extract_number_from_string(s):
    # Define a regex pattern to match the string 'getcar/' followed by digits
    pattern = r'^getcar/(\d+)$'

    # Search for the pattern in the input string
    match = re.match(pattern, s)

    if match:
        # Extract the number from the match object
        number = match.group(1)
        return int(number)
    else:
        # Return None or handle the case where the pattern is not matched
        return None


def json_to_string(json_object):
    # Convert JSON object to string
    json_string = json.dumps(json_object)

    return json_string

def hex_to_json(hex_string):
    # Remove '0x' prefix if present
    if hex_string.startswith('0x'):
        hex_string = hex_string[2:]

    # Convert hex string to bytes
    byte_data = binascii.unhexlify(hex_string)

    # Convert bytes to string (assuming UTF-8 encoding)
    json_string = byte_data.decode('utf-8')


    try:
        # Attempt to parse the input string as JSON
        json_object = json.loads(json_string)
        return json_object
    except json.JSONDecodeError:
        # If parsing fails, return the input string as is
        return json_string


def string_to_hex(s):
    # Encode the string to bytes
    byte_string = s.encode('utf-8')

    # Convert bytes to hexadecimal representation
    hex_string = binascii.hexlify(byte_string).decode('utf-8')

    # Add the '0x' prefix
    hex_with_prefix = '0x' + hex_string

    return hex_with_prefix


def hex_to_string(hex_string):
    # Remove '0x' prefix if present
    if hex_string.startswith('0x'):
        hex_string = hex_string[2:]

    # Convert hex string to bytes
    bytes_object = bytes.fromhex(hex_string)

    # Convert bytes to string
    string = bytes_object.decode('utf-8')

    return string


def handle_advance(data):
    global total
    logger.info(f"Received advance request data {data}")
    logger.info("Adding notice")
    notice = {"payload": data["payload"]}
    response = requests.post(rollup_server + "/notice", json=notice)
    logger.info(f"Received notice status {response.status_code} body {response.content}")

    metadata = data['metadata']
    sender = metadata["msg_sender"]
    payload = data["payload"]

    json_data = hex_to_json(payload)
    _id = len(cars) + 1

    if type(json_data) == str:
        if json_data.isdigit():
            notice = {"payload": string_to_hex("Car name is not on hex format: i.e Numeric")}
            response = requests.post(rollup_server + "/report", json=notice)
            logger.info(f"Received notice status {response.status_code} body {response.content}")
            return "reject"
        else:
            readable_time = unix_timestamp_to_datetime(metadata['timestamp'])
            cars.append({"id":_id, 'lister': sender, "car_name": json_data, "listing_ts": readable_time,
                         "block_num": metadata['block_number']})
            total += 1

            car_name = json_data.upper()
            notice = {"payload": string_to_hex(car_name)}
            response = requests.post(rollup_server + "/notice", json=notice)
            logger.info(f"Received notice status {response.status_code} body {response.content}")

            return "accept"

    else:
        try:
            readable_time = unix_timestamp_to_datetime(metadata['timestamp'])
            cars.append({"id":_id, 'lister':sender,"car_name":json_data['name'], "listing_ts":readable_time,
                         "block_num":metadata['block_number'], "car_price":json_data['price'], "car_desc": json_data['desc']})
            total += 1

            car_name = json_data['name']
            notice = {"payload": string_to_hex(car_name)}
            response = requests.post(rollup_server + "/notice", json=notice)
            logger.info(f"Received notice status {response.status_code} body {response.content}")

            return "accept"
        except:
            notice = {"payload": string_to_hex("Error: Invalid Json format or parameters")}
            response = requests.post(rollup_server + "/notice", json=notice)
            logger.info(f"Received notice status {response.status_code} body {response.content}")


def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    report = {"payload": data["payload"]}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")

    string = hex_to_string(data['payload'])

    responseObject = ""
    if string == "getAllCars":
        responseObject = json.dumps(cars)
    elif string == "totallisting":
        responseObject = str(total)
    elif extract_number_from_string(string):
        for i in cars:
            if i['id'] == extract_number_from_string(string):
                responseObject = json_to_string(i)
    else:
        responseObject = "Route not implemented!"

    report = {"payload": string_to_hex(responseObject)}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")

    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
