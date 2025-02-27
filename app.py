from fastapi import FastAPI
from request_methods import NseData

# FastAPI
app = FastAPI()

# Creating Object
req_api = NseData()

# Home Page
@app.get("/")
def homepage():

    # Setting Cookies
    req_api.setCookie()

    # Downloading Csv
    req_api.downloadCsv()
    return {"status":"success",
            "status_code": 200,
            "message": "file downloaded"}

# Download File
@app.get("/combinecsv")
def filedownload():

    # Combining Dataframe
    req_api.combineDataframe()
    return {"status":"success",
            "status_code": 200,
            "message": "combined successfully"}

# Calculation
@app.get("/calculation")
def calculate():

    # Performing Calculation
    req_api.dataframeCalculation()
    return {"status":"success",
            "status_code": 200,
            "message":"notification sent successfully"}