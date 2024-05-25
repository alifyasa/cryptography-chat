from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils.constant import METHOD
from utils.mode.mode import Mode
from utils.logging import pprint
from utils.types import *
from utils.helper import *
from utils.cipher.service import *

app = Flask(__name__)
CORS(app)
mode = Mode(bit="", key="", mode_method=METHOD['ECB'], encryption_length=0)

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
  print("=" * 33, "ENCRYPT", "=" * 33)

  # Input
  data, file_name = get_request_mode(request,0)
  # Output
  mode.set_bit(data['inputBit'])
  mode.set_key(data['keyBit'])
  mode.set_mode_method(data['method'])

  if data['method'] == METHOD['CFB'] or data['method'] == METHOD['OFB']:
    mode.set_encryption_length(data['encryptionLength'])

  pprint("Input Bit Padded", data['inputBit'])
  encrypted_data = mode.encrypt()
  pprint("Encrypted Data", encrypted_data)

  execution_time = mode.get_time_execution()

  result = get_output_result(request.form, encrypted_data, 0, file_name)

  res = ResponseResult(time=execution_time, result=result)

  # print(res)

  return jsonify(res)

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
  print("=" * 33, "DECRYPT", "=" * 33)
  # Input
  data, file_name = get_request_mode(request,1)

  # Output
  mode.set_bit(data['inputBit'])
  mode.set_key(data['keyBit'])
  mode.set_mode_method(data['method'])

  if data['method'] == METHOD['CFB'] or data['method'] == METHOD['OFB']:
    mode.set_encryption_length(data['encryptionLength'])

  decrypted_data = mode.decrypt()
  pprint("Decrypted Data", decrypted_data)

  execution_time = mode.get_time_execution()

  result = get_output_result(request.form, decrypted_data, 1, file_name)
  if len(result) <= 20:
    print(f"{'Decrypted Text':<20} - {result}")
  else:
    print(f"{'Decrypted Text':<20} - {result[:30]}...{result[-30:]}")

  res = ResponseResult(time=execution_time, result=result)

  return jsonify(res)

@app.route('/api/output/<path:filename>')
def serve_assets(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
  app.run()