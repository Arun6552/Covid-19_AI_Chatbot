from chatbot.exception import ChatbotException
from chatbot.logger import logging
from chatbot.send_email import EMailClient
import sys

def prepareEmail(contact_list):
    try:
        mailclient = EMailClient.GMailClient()
    
        mailclient.sendEmail(contact_list)
        logging.info("mail sent successfully.....")
    except Exception as e:
        raise ChatbotException(e,sys) from e
    