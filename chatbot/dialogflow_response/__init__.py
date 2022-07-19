#python module import
from flask import request,make_response
import json
import sys
from datetime import datetime

#custom module import
from chatbot.exception import ChatbotException
from chatbot.logger import logging
from chatbot.db_config import configureDataBase
from chatbot.api_request import makeAPIRequest
from chatbot.save_chats import DBChats
from chatbot.send_email.prepare_email import prepareEmail




def webhooks():
    try:
        req = request.get_json(silent=True, force=True)
        res = processRequest(req)
        res = json.dumps(res, indent=4)
        # print(res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'

    except Exception as e:
        raise ChatbotException(e,sys) from e

    return r
    
    
saveCases_sessionID = 0
cust_country = None
# processing the request from dialogflow
def processRequest(req):
    log = DBChats()
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    parameters = result.get("parameters")
    cust_name = parameters.get("cust_name")
    cust_contact = parameters.get("cust_contact")
    cust_email = parameters.get("cust_email") 
    
    #Datetime 
    now = datetime.now()
    dt_now = now.strftime("%Y/%m/%d %H:%M:%S")
    print(dt_now)
    
    #Database config
    db = configureDataBase()
    
    if intent == 'covid_searchcountry':
        global cust_country

        cust_country = parameters.get("geo-country")
        if(cust_country=="United States"):
            cust_country = "USA"
        try:
            fulfillmentText, deaths_data, testsdone_data = makeAPIRequest(cust_country)

        except Exception as e:
            raise ChatbotException(e,sys) from e
        
        # print(deaths_data,testsdone_data)
        # print(fulfillmentText)
        webhookresponse = "***Covid Report*** \n\n" +  "******* Country : " + cust_country + " ******* "+ "\n\n" +" New cases :" + str(fulfillmentText.get('new')) + \
                          "\n" + " Active cases : " + str(
            fulfillmentText.get('active')) + "\n" + " Critical cases : " + str(fulfillmentText.get('critical')) + \
                          "\n" + " Recovered cases : " + str(
            fulfillmentText.get('recovered')) + "\n" + " Total cases : " + str(fulfillmentText.get('total')) + \
                          "\n" + " Total Deaths : " + str(deaths_data.get('total')) + "\n" + " New Deaths : " + str(
            deaths_data.get('new')) + \
                          "\n" + " Total Test Done : " + str(testsdone_data.get('total'))+ "\n\n*******This report is generated at " + dt_now + " ******* " + "\n\n*******END********* \n "
                          
        new_case = str(fulfillmentText.get('new'))
        active_cases = str(fulfillmentText.get('active'))
        critical_cases = str(fulfillmentText.get('critical'))
        recovered_cases = str(fulfillmentText.get('recovered'))
        total_cases =  str(fulfillmentText.get('total'))
        total_test_cases = str(testsdone_data.get('total'))
        total_death_cases =  str(deaths_data.get('total'))

        
        print(webhookresponse)
        log.saveConversations(sessionID, cust_country, webhookresponse, intent, db)
        logging.info("Conversation saved !!!")
        
        global saveCases_sessionID
        saveCases_sessionID =sessionID
        log.saveCases(saveCases_sessionID,cust_country,new_case,active_cases,critical_cases,recovered_cases,total_cases,total_test_cases,total_death_cases, db)
        logging.info("Cases  saved !!!")
        return {

                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": [
                                    webhookresponse
                                ]

                            }
                        },
                        {
                            "text": {
                                "text": [
                                    "Do you want me to send the detailed report to your e-mail address? Type.. \n 1. Sure \n 2. Not now "
                                    # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                                ]

                            }
                        }
                    ]
                }
    elif intent == "Welcome" or intent == "continue_conversation" or intent == "not_send_email" or intent == "endConversation" or intent == "Fallback" or intent == "covid_faq" or intent == "select_country_option":
        try:
            fulfillmentText = result.get("fulfillmentText")
            log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)
            logging.info("Conversation saved !!!")

        except Exception as e:
            raise ChatbotException(e,sys) from e
        
    elif intent == "send_report_to_email":
        try:
            fulfillmentText = result.get("fulfillmentText")
            log.saveConversations(sessionID, "Sure send email", fulfillmentText, intent, db)
            val = log.getcasesForEmail(saveCases_sessionID, db)
            prepareEmail([cust_name, cust_contact, cust_email,val])
            logging.info("Email Preparing.....")

        except Exception as e:
            raise ChatbotException(e,sys) from e
        
    elif intent == "totalnumber_cases":
        try:
            fulfillmentText = makeAPIRequest("world")

            webhookresponse = "***World wide Report*** \n\n" + " Confirmed cases :" + str(
                fulfillmentText.get('confirmed')) + \
                            "\n" + " Deaths cases : " + str(
                fulfillmentText.get('deaths')) + "\n" + " Recovered cases : " + str(fulfillmentText.get('recovered')) + \
                            "\n" + " Active cases : " + str(
                fulfillmentText.get('active')) + "\n" + " Fatality Rate : " + str(
                fulfillmentText.get('fatality_rate') * 100) + "%" + \
                            "\n" + " Last updated : " + str(
                fulfillmentText.get('last_update')) + "\n\n*******This report is generated at " + dt_now + " ******* "+ "\n\n*******END********* \n "
            print(webhookresponse)
            log.saveConversations(sessionID, "Cases worldwide", webhookresponse, intent, db)
            # log.saveCases("world", fulfillmentText, db)   
            logging.info("Conversation saved !!!")
            return {

                        "fulfillmentMessages": [
                            {
                                "text": {
                                    "text": [
                                        webhookresponse
                                    ]

                                }
                            },
                            {
                                "text": {
                                    "text": [
                                        "Do you want me to send the detailed report to your e-mail address? Type.. \n 1. Sure \n 2. Not now "
                                        # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                                    ]

                                }
                            }
                        ]
                    }
        except Exception as e:
            raise ChatbotException(e,sys) from e
        
    

    elif intent == "covid_searchstate":
        try:
            fulfillmentText = makeAPIRequest("state")
            print(len(fulfillmentText))

            webhookresponse1 = ''
            webhookresponse2 = ''
            webhookresponse3 = ''
            for i in range(0,11):
                webhookresponse = fulfillmentText[i]
                # print(webhookresponse['state'])
                # js = json.loads(webhookresponse.text)

                # print(str(js.state))
                webhookresponse1 += "*********\n" + " State :" + str(webhookresponse['state']) + \
                                    "\n" + " Confirmed cases : " + str(
                    webhookresponse['confirmed']) + "\n" + " Death cases : " + str(webhookresponse['deaths']) + \
                                    "\n" + " Active cases : " + str(
                    webhookresponse['active']) + "\n" + " Recovered cases : " + str(
                    webhookresponse['recovered']) + "\n*********"
            for i in range(11, 21):
                webhookresponse = fulfillmentText[i]
                # print(webhookresponse['state'])
                # js = json.loads(webhookresponse.text)

                # print(str(js.state))
                webhookresponse2 += "*********\n" + " State :" + str(webhookresponse['state']) + \
                                    "\n" + " Confirmed cases : " + str(
                    webhookresponse['confirmed']) + "\n" + " Death cases : " + str(webhookresponse['deaths']) + \
                                    "\n" + " Active cases : " + str(
                    webhookresponse['active']) + "\n" + " Recovered cases : " + str(
                    webhookresponse['recovered']) + "\n*********"
            for i in range(21, 38):
                webhookresponse = fulfillmentText[i]
                # print(webhookresponse['state'])
                # js = json.loads(webhookresponse.text)

                # print(str(js.state))
                webhookresponse3 += "*********\n" + " State :" + str(webhookresponse['state']) + \
                                    "\n" + " Confirmed cases : " + str(
                    webhookresponse['confirmed']) + "\n" + " Death cases : " + str(webhookresponse['deaths']) + \
                                    "\n" + " Active cases : " + str(
                    webhookresponse['active']) + "\n" + " Recovered cases : " + str(
                    webhookresponse['recovered']) + "\n*********"
            print("***India State Report*** \n\n" + webhookresponse1 + "*******This report is generated at " + dt_now + " ******* "+ "\n\n*******END********* \n")
            print("***India State Report*** \n\n" + webhookresponse2 + "*******This report is generated at " + dt_now + " ******* "+ "\n\n*******END********* \n")
            print("***India State Report*** \n\n" + webhookresponse3 + "*******This report is generated at " + dt_now + " ******* "+ "\n\n*******END********* \n")



            log.saveConversations(sessionID, "Indian State Cases", webhookresponse1, intent, db)
            return {

                        "fulfillmentMessages": [
                            {
                                "text": {
                                    "text": [
                                        webhookresponse1
                                    ]

                                }
                            },
                            {
                                "text": {
                                    "text": [
                                        webhookresponse2
                                    ]

                                }
                            },
                            {
                                "text": {
                                    "text": [
                                        webhookresponse3
                                    ]

                                }
                            },
                            {
                                "text": {
                                    "text": [
                                        "Do you want me to send the detailed report to your e-mail address? Type.. \n 1. Sure \n 2. Not now "
                                        # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                                    ]

                                }
                            }
                        ]
                    }

        except Exception as e:
            raise ChatbotException(e,sys) from e
    else:
        return {
            "fulfillmentText": "something went wrong,Lets start from the begning, Say Hi",
        }
    logging.info("Dialogflow file Run successfully.....")
    
    