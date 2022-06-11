import requests
import schedule

def rcp():
    requests.get('https://eris-modo-bot.herokuapp.com/')

schedule.every(10).minutes.do(rcp)

while True:
    schedule.run_pending()