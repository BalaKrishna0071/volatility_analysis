import logging
import os
from config import csv_path
from loggers import handler
from req_methods import NseData

# # Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Checking if Folders Exists or Not
if not os.path.exists(csv_path):
    os.mkdir(csv_path)
    logger.info("-----------------------------------------------")
    logger.info("Folder Created ! ")

else:
    logger.info("-----------------------------------------------")
    logger.info("Folder Already Exists ! ")


# Creating Object
req_api = NseData()

# global variable
global UserInput

while True:
    logger.info("-----------------------------------------------")
    logger.info("Download BhavCopy & Volatatily file ! 1")
    logger.info("Combine Dataframe ! 2")
    logger.info("Dataframe Calculation ! 3")
    logger.info("Exit ! 0")
    logger.info("Enter Number :\n")

    UserInput = int(input())

    match UserInput:
        case 1:
            logger.info("Executing...")
            req_api.setCookie()
            req_api.downloadCsv()
            logger.info("Downloaded Csv !!!")
        case 2:
            logger.info("Executing...")
            req_api.combineDataframe()
            logger.info("Downloaded Csv !!!")
        case 3:
            logger.info("Executing...")
            req_api.dataframeCalculation()
            logger.info("Downloaded Csv !!!")
        case 0:
            exit()
