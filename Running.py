#This file isn't neccessary. Delete if you have your own hosting. The purpose of this bot is to ping the host via uptimebot.com every minute or so to keep it alive. 

from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
  return "Hello."

def run():
  app.run(host='0.0.0.0',port=8080)

def running():
    t = Thread(target=run)
    t.start()
