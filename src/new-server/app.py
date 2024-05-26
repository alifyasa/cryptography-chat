from constant import UNIQUE_CODE
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from services.ecdh import get_all_key_ECDH
from services.schnorr_generate import SCHNORR_ALPHA, SCHNORR_P, SCHNORR_Q
from sqlalchemy import create_engine
import os
import pandas as pd
import json
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

mysql_engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
bob_private_key, bob_public_key, alice_private_key, alice_public_key, alice_shared_secret = get_all_key_ECDH()
print(alice_shared_secret)

@app.route('/api/shared-key/validation', methods=['POST'])
def validate_shared_key():
  payload = request.json
  shared_key = payload['shared_key']

  if shared_key == str(alice_shared_secret):
    return jsonify({'is_valid': True, 'message': 'Shared key is valid!'})
  else:
    return jsonify({'is_valid': False, 'message': 'Shared key is invalid!'})

@app.route('/api/shared-key', methods=['GET'])
def get_shared_key():
  return jsonify({'shared_key': str(alice_shared_secret)})

@app.route('/api/chats', methods=['GET'])
def get_chats():
  query = "SELECT * FROM chats"
  df = pd.read_sql(query, con=mysql_engine)

  return df.to_json(orient='records')

@app.route('/api/chats', methods=['POST'])
def send_chat():
  payload = request.json
  df = pd.DataFrame([payload])

  # Decrypt ALS
  if payload['message'].startswith(UNIQUE_CODE['ALS']):
    url = os.getenv('BLOCK_CIPHER_API') + '/decrypt'
    print(payload['message'][len(UNIQUE_CODE['ALS']):])
    block_cipher_payload = {
      'inputText': payload['message'][len(UNIQUE_CODE['ALS']):],
      'method': 'ECB',
      'key': str(alice_shared_secret),
      'encryptionLength': 1
    }
    response = requests.post(url, json=block_cipher_payload)
    result = json.loads(response.json()['result'])

    df = pd.DataFrame([result])

  # Insert to database
  df.to_sql('chats', con=mysql_engine, if_exists='append', index=False)
  
  return jsonify({'message': 'Chat sent!'})

@app.route('/schnorr-pkey', methods=['GET'])
def get_schnorr_pkey():
  return jsonify({
    'alpha': SCHNORR_ALPHA,
    'p': SCHNORR_P,
    'q': SCHNORR_Q
  })

if __name__ == '__main__':
  app.run(port=os.getenv('PORT'))