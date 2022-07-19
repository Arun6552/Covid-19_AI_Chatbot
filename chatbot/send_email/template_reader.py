import sys
import os

from chatbot.exception import ChatbotException
from chatbot.logger import logging

     
class TemplateReader:
    def __init__(self):
        pass

    def read_course_template(self,course_name):
        try:
            if (course_name=='report'):
                email_file = open("sendEmail/graphs.html", "r")
                email_message = email_file.read()

            elif (course_name == 'country'):
                email_file = open("sendEmail/DLM_Template.html", "r")
                email_message = email_file.read()
            elif (course_name == 'country_cases'):
                email_file = open("chatbot/send_email/country_cases.html", "r")
                email_message = email_file.read()
                logging.info("file read successfully")
            return email_message
        except Exception as e:
            raise ChatbotException(e,sys) from e

