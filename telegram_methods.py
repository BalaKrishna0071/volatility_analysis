import os
import requests
from dotenv import load_dotenv

# loading .env
load_dotenv()
apitoken = os.getenv('APITOKEN')

class Telegram:

    def __init__(self):
        self.chat_id = None

    # get updates
    def getUp(self):
        url = f'https://api.telegram.org/bot{apitoken}/getUpdates'
        res = requests.get(url=url).json()
        self.chat_id = res["result"][0]["message"]["chat"]["id"]

    # send message
    def sendMsg(self,message: str):
        url = f'https://api.telegram.org/bot{apitoken}/sendMessage'
        d1 = {'chat_id': self.chat_id, 'text': message}
        requests.post(url=url, data=d1).json()




