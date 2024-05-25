import base64
import os

from utils.convert import string_to_byte_string, block_string_to_byte_string
from utils.logging import pprint

# Input
def get_request_mode(request,mode_operation):
    file_name = ""
    if request.form:
        data = request.form.to_dict()
        file = request.files['inputFile']
        file_name = file.filename
        data['inputBit'] = ''.join(format(byte, '08b') for byte in file.read())
        data['encryptionLength'] = int(data['encryptionLength'])
    else:
        data = request.get_json()
        if len(data['inputText']) <= 20:
            print(f"{'Input Text Raw':<20} - {data['inputText']}")
        else:
            print(f"{'Input Text Raw':<20} - {data['inputText'][:30]}...{data['inputText'][-30:]}")

        # Convert text to bit
        if(mode_operation==1):
            data['inputText'] = base64.b64decode(data['inputText'].encode()).decode()

        # data['inputBit'] = ''.join(format(ord(char), '08b') for char in data['inputText'])
        data['inputBit'] = string_to_byte_string(data['inputText'])
        pprint("Input Bit Raw", data['inputBit'])
        while len(data['inputBit']) % 128 != 0:
            data['inputBit'] = "0" + data['inputBit']

    # Convert key to bit
    data['keyBit'] = ''.join(format(ord(char), '08b') for char in data['key'])

    return data, file_name

# Output
def bit_to_file(file_name, text, mode_operation):
    if mode_operation == 0:
        root_dir = 'output/[ENCRYPTED]'
        mode = 'encrypted'
    else:
        root_dir = 'output/[DECRYPTED]'
        mode = 'decrypted'

    result = bytes([int(text[i:i+8], 2) for i in range(0, len(text), 8)])
    file_path = f'{root_dir} {file_name}'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as file:
        file.write(result)

    result = f"{file_path}"

    return result

def bit_to_text(text, mode_operation):

    if mode_operation == 0: # Enkrip
        byte_array = text
    else: # Dekrip
        byte_array = block_string_to_byte_string(text)

    pprint("Byte to Text", byte_array)

    result = ''

    for i in range(0, len(byte_array), 8):
        result += chr(int(byte_array[i:i+8], 2))

    # Encode the string into base64
    if(mode_operation == 0):
        result = base64.b64encode(result.encode()).decode()

    return result

def get_output_result(form, text, mode_operation, file_name):
    if form:
        res = bit_to_file(file_name, text, mode_operation)
    else:
        res = bit_to_text(text, mode_operation)
    return res