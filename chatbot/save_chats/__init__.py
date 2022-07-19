from datetime import datetime
import sys

#Custom module Import
from chatbot.exception import ChatbotException
from chatbot.logger import logging



class DBChats:
    def __init__(self):
        pass

    def saveConversations(self, sessionID, usermessage,botmessage,intent,dbConn):

        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

        mydict = {"sessionID":sessionID,"User Intent" : intent ,"User": usermessage, "Bot": botmessage, "Date": str(self.date) + "/" + str(self.current_time)}

        try:
            records = dbConn.chat_records
            records.insert_one(mydict)
            logging.info("Saved Conversation to Database")

        except Exception as e:
            raise ChatbotException(e,sys) from e


    def saveCases(self,sessionID,cust_country,new_case,active_cases,critical_cases,recovered_cases,total_cases,total_test_cases,total_death_cases,dbConn):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

        cases_dict = {  'sessionID' :sessionID,
                        'cust_country':cust_country,
                        'cases_data': {
                                        'new_case':new_case, 
                                        'active_cases':active_cases,
                                        'critical_cases':critical_cases,
                                        'recovered_cases':recovered_cases,
                                        'total_cases':total_cases,
                                        'total_test_cases':total_test_cases,
                                        'total_death_cases':total_death_cases   
                                    },
                        "Date": str(self.date) + "---" + str(self.current_time)
                    }
        try:
            records = dbConn.cases_records
            records.insert_one(cases_dict)
            logging.info("Saved Cases to Database")

        except Exception as e:
            raise ChatbotException(e,sys) from e

    def getcasesForEmail(self, sessionID,dbConn):
        try:
            records = dbConn.cases_records
        except Exception as e:
            raise ChatbotException(e,sys) from e
        logging.info("Searching sessionID into Database....")
        return records.find_one({'sessionID': sessionID})