import requests
import threading

def rcp():
    threading.Timer(10, rcp).start()
    requests.get('https://eris-modo-bot.herokuapp.com/')

rcp()