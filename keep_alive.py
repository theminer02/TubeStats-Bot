from flask import Flask
from threading import Thread
# from main import displayServers

app = Flask('')

@app.route('/')
def home():
  return "Bot is alive.\n" # + displayServers

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
