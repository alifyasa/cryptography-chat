from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from services.ecdh import getAllKeyECDH
from sqlalchemy import create_engine
import os
import pandas as pd

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

mysql_engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
bob_private_key, bob_public_key, alice_private_key, alice_public_key, alice_shared_secret = getAllKeyECDH()

@app.route('/api/shared-key', methods=['GET'])
def get_shared_key():
  return jsonify({'shared_key': alice_shared_secret})

@app.route('/api/chats', methods=['GET'])
def get_chats():
  query = "SELECT * FROM chats"
  df = pd.read_sql(query, con=mysql_engine)

  return df.to_json(orient='records')

@app.route('/api/chats', methods=['POST'])
def send_chat():
  payload = request.json
  df = pd.DataFrame([payload])
  df.to_sql('chats', con=mysql_engine, if_exists='append', index=False)
  
  return jsonify({'message': 'Chat sent!'})

if __name__ == '__main__':
  app.run()