import requests
import json
import sys

#Custom module Import
from chatbot.exception import ChatbotException
from chatbot.logger import logging

class Api():
    def __init__(self):
        pass 
    
    #Api request for Country
    def makeApiRequestForCounrty(self, country_name):
        url = "https://covid-193.p.rapidapi.com/statistics"
        querystring = {"country": country_name}
        headers = {
                    "X-RapidAPI-Key": "c907bc661dmshad30c509ef7f277p187f90jsnf837ee140327",
                    "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
                }
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            logging.info("Country-Data response successfully from RapidAPI")
        except Exception as e:
            raise ChatbotException(e,sys) from e
        # print(response.text)
        js = json.loads(response.text)
        # print("js******", js)
        result = js.get('response')[0]
        # print(result.get('cases'))
        # print("*" * 20)
        return result.get('cases') , result.get('deaths'),result.get('tests') 
    
    def makeApiRequestForHistoryData(self):
        url = "https://covid19-data.p.rapidapi.com/history"
        querystring = {"country":"usa","day":"2020-06-02"}
        headers = {
                    "X-RapidAPI-Key": "c907bc661dmshad30c509ef7f277p187f90jsnf837ee140327",
                    "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
                }
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            logging.info("history-Data response successfully from RapidAPI")
        except Exception as e:
            raise ChatbotException(e,sys) from e
        # print(response.text)
        js = json.loads(response.text)
        # print("******", js)
        #result = js.get('list')
        # logging.info("Api request for Histroy Data Covid19 is successful")
        return js
    
    def makeApiRequestForIndianStates(self):
        url = "https://covid19-data.p.rapidapi.com/india"
        headers = {
            'x-rapidapi-host': "covid19-data.p.rapidapi.com",
            'x-rapidapi-key': "482a8f8516msh16204eb9d1f4f68p1a9146jsnf33914c7300e"
        }
        try:
            response = requests.request("GET", url, headers=headers)
        except Exception as e:
            raise ChatbotException(e,sys) from e
        # print(response.text)
        js = json.loads(response.text)
        # print("******", js)
        #result = js.get('list')
        logging.info("India-State Data response successfully from RapidAPI")
        return js
    
    def makeApiWorldwide(self):
        url = "https://covid-19-statistics.p.rapidapi.com/reports/total"
        headers = {
            "x-rapidapi-host": "covid-19-statistics.p.rapidapi.com",
            "x-rapidapi-key": "482a8f8516msh16204eb9d1f4f68p1a9146jsnf33914c7300e"
        }
        try:
            response = requests.request("GET", url, headers=headers)
            logging.info("world-wide-Data response successfully from RapidAPI")
        except Exception as e:
            raise ChatbotException(e,sys) from e
        # print(response.text)
        js = json.loads(response.text)
        # print("******", js)
        result = js.get('data')
        # logging.info("Api request for world wide  is successful")
        return result
    
    
def makeAPIRequest(query):
    api = Api()
    if query == "world":
        return api.makeApiWorldwide()
    if query == "state":
        return api.makeApiRequestForIndianStates()
    else:
        return api.makeApiRequestForCounrty(query)    
    
    
    
    

