import os
import smtplib
import  sys
from email.message import EmailMessage

from chatbot.exception import ChatbotException
from chatbot.logger import logging

from . import template_reader

class GMailClient:
    def __init__(self):
        pass
    def sendEmail(self,contacts):
        EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
        # EMAIL_ADDRESS = 'sender email id'
        # EMAIL_PASSWORD = 'password'
        print(EMAIL_ADDRESS,EMAIL_PASSWORD)

        msg = EmailMessage()
        msg['Subject'] = 'Detailed Covid-19 Report!'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = contacts[2]

        value = contacts[3]
        values = value.get("cases_data")
        # print(values)
        msg.set_content("Hello Mr. {} Here is your Covid 19 Report PFA".format(contacts[0]))
        # print(msg.text)
        try:
            template = template_reader.TemplateReader()
            email_message = template.read_course_template("country_cases")
        except Exception as e:
            raise ChatbotException(e,sys) from e
        cust_name = contacts[0]
        # print(cust_name)
        country_name = str(value.get("cust_country"))  #"India"

 
        total_cases1 = str(values.get("total_cases"))
        new_case1 = str(values.get("new_case"))
        active_cases1 = str(values.get("active_cases"))
        critical_cases1 = str(values.get("critical_cases"))
        recovered_cases1 = str(values.get("recovered_cases"))
        total_test_cases1 = str(values.get("total_test_cases"))
        total_death_cases1 = str(values.get("total_death_cases"))
        date_at = str(value.get("Date"))
        
        logging.info("fetching data from db successfully",total_cases1,new_case1,critical_cases1,recovered_cases1,total_test_cases1,total_death_cases1,date_at)

        try:
            msg.add_alternative(email_message.format(country_name=country_name, total_cases=total_cases1, new_case=new_case1, active_cases=active_cases1, critical_cases=critical_cases1,
                                        recovered_cases=recovered_cases1,total_test_cases=total_test_cases1,total_death_cases=total_death_cases1,cust_name=cust_name,date_at=date_at), subtype='html')
            
 
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    smtp.send_message(msg)
                    logging.info("email sent successfully")
        
        except Exception as e:
            raise ChatbotException(e,sys) from e

    
    
    
    

