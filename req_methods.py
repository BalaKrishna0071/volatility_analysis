import datetime
import logging
import os.path
import pandas as pd
import requests
from config import csv_path
from mail import mailSend
from logger import logger
from telegram_methods import Telegram

# logger = logging.getLogger(__name__)

# File Paths
csv_one = os.path.join(csv_path, "BhavCopy.csv")
csv_two = os.path.join(csv_path, "Volatility.csv")
csv_three = os.path.join(csv_path, "DataSheet.csv")
csv_four = os.path.join(csv_path, "Result.csv")
csv_five = os.path.join(csv_path, "Final.csv")

telegram_api = Telegram()

class NseData:
    home_page_url = "https://www.nseindia.com/"

    #  Header for GET Request
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://www.nseindia.com/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    def __init__(self):
        self.cookie = None

    # Functions for Setting Cookie
    def setCookie(self):
        try:
            api_res = requests.get(url=self.home_page_url, headers=self.headers)
            if api_res.status_code == 200:
                self.cookie = api_res.cookies
            else:
                print(f"error while setting cookie {api_res.status_code}")
        except Exception as err:
            print("error while running get request", err)


    # Functions for Downloading Csv Files
    def downloadCsv(self):

        # Accepting Custom Date
        input_date = str(input("Enter Date\n"))
        date = datetime.datetime.strptime(input_date, "%d/%m/%Y")
        day = date.strftime("%A")

        # Checking if Day is Sat or Sun
        if day == "Saturday" or day == "Sunday":
            new_date = date - datetime.timedelta(days=2)
            old_date = new_date.strftime("%Y%m%d")
            old_date_rev = new_date.strftime("%d%m%Y")
        else:
            old_date = date.strftime("%Y%m%d")
            old_date_rev = date.strftime("%d%m%Y")

        # Retrieving csv files from Get Request
        response_one = requests.get(f"https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{old_date}_F_0000.csv.zip",headers=self.headers, cookies=self.cookie, stream=True)
        response_two = requests.get(f"https://nsearchives.nseindia.com/archives/nsccl/volt/CMVOLT_{old_date_rev}.CSV", headers=self.headers, cookies=self.cookie, stream=True)

        # If Status Code is 200 Then  Writing
        if response_one.status_code == 200 and response_two.status_code == 200:
            logger.info("Successfully Downloaded !")
            res_content1 = response_one.content
            res_content2 = response_two.content
            csv_file1 = open(csv_one, "wb+")
            csv_file2 = open(csv_two, "wb+")
            csv_file1.write(res_content1)
            csv_file2.write(res_content2)
            csv_file1.close()
            csv_file2.close()
            logger.info("Executed !")
        else:
            logger.info("Error")


    # Function for Combining
    def combineDataframe(self):

        # Reading Both Dataframe
        dataframe1 = pd.read_csv(csv_one, compression='zip')
        dataframe2 = pd.read_csv(csv_two)

        # Creating a New Dataframe
        combineDataframe = pd.DataFrame()
        combineDataframe = dataframe1.join(dataframe2)

        # Converting Dataframe into Csv File
        combineDataframe.to_csv(csv_three)


    # Function for Performing Calculation
    def dataframeCalculation(self):

        # Calculation one HighPrice
        datasheetDataframe = pd.read_csv(csv_three)
        datasheetDataframe['prevday'] = datasheetDataframe['Previous Day Underlying Volatility (D)'] * datasheetDataframe['ClsPric']
        datasheetDataframe['step1'] = datasheetDataframe['ClsPric'] + datasheetDataframe['prevday']
        datasheetDataframe['step2'] = 0.99 * datasheetDataframe['step1']
        datasheetDataframe['High_Price'] = datasheetDataframe['HghPric'] > datasheetDataframe['step2']

        # Calculation two LowPrice
        datasheetDataframe['prevday2'] = datasheetDataframe['Previous Day Underlying Volatility (D)'] * datasheetDataframe['ClsPric']
        datasheetDataframe['step1'] = datasheetDataframe['ClsPric'] - datasheetDataframe['prevday2']
        datasheetDataframe['step2'] = 1.01 * datasheetDataframe['step1']
        datasheetDataframe['Low_Price'] = datasheetDataframe['LwPric'] > datasheetDataframe['step2']

        # Under_Range
        datasheetDataframe['Under_Range'] = datasheetDataframe.apply(lambda x: x['High_Price'] and x['Low_Price'],axis=1)

        # Converting Dataframe into Csv file
        datasheetDataframe.to_csv(csv_four, index=False)

        # Sorting Under_range Column
        df = pd.DataFrame(datasheetDataframe)
        sortDf = df.loc[(datasheetDataframe['Under_Range'] == True)]

        # Converting into List
        d = sortDf['TckrSymb'].to_list()

        subj = str(input("Enter Subject :"))
        recip = str(input("Enter Mail Id :"))

        # Sending Sorted Symbols
        for symbols in [d[i:i + 50] for i in range(0, len(d), 50)]:
            msgStr = '\n'.join(symbols)
            telegram_api.sendMsg(msgStr)
            mailSend(message=msgStr,subject=subj, recipient=recip)




