
import json
import binascii

def string_to_hex():
    #Example String Object
    example = "FORD"

    # Encode the string to bytes
    byte_string = example.encode('utf-8')

    # Convert bytes to hexadecimal representation
    hex_string = binascii.hexlify(byte_string).decode('utf-8')

    # Add the '0x' prefix
    hex_with_prefix = '0x' + hex_string

    return hex_with_prefix


def json_to_hex():
    # Example JSON object
    example = {
        "name": "Ford",
        "price": 6,
        "desc": "2024 model"
    }

    # Convert JSON object to a JSON string
    json_string = json.dumps(example)

    # Encode the JSON string to bytes
    byte_data = json_string.encode('utf-8')

    # Convert bytes to a hexadecimal string
    hex_string = binascii.hexlify(byte_data).decode('utf-8')

    # Add the '0x' prefix to the hexadecimal string (optional)
    hex_with_prefix = '0x' + hex_string

    return hex_with_prefix

def hex_to_string():
    #Example Hex object
    example = "0x466f7264"

    # Remove '0x' prefix if present
    hex_string = example[2:]

    # Convert hex string to bytes
    bytes_object = bytes.fromhex(hex_string)

    # Convert bytes to string
    string = bytes_object.decode('utf-8')

    return string


def hex_to_json():
    #Example Hex object
    example = "0x7b226964223a20362c20226c6973746572223a2022307866333966643665353161616438386636663463653661623838323732373963666666623932323636222c20226361725f6e616d65223a20224368657665726f6e222c20226c697374696e675f7473223a2022323032342d30382d30322031383a33313a3135222c2022626c6f636b5f6e756d223a203531357d"

    # Remove '0x' prefix if present
    hex_string = example[2:]

    # Convert hex string back to bytes
    byte_data = binascii.unhexlify(hex_string)

    # Decode bytes to JSON string
    json_string = byte_data.decode('utf-8')

    # Convert JSON string back to list of dictionaries
    json_object = json.loads(json_string)

    return json_object


#Convert String to Hex
str_representation = string_to_hex()
print(str_representation)

#Convert Hex to String
hexstr_representation = hex_to_string()
print(hexstr_representation)

# Convert JSON to hex
hex_representation = json_to_hex()
print(hex_representation)

#Convert Hex to JSON
json_representation = hex_to_json()
print(json_representation)
