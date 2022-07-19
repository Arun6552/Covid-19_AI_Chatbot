from pymongo import MongoClient
import sys

from chatbot.exception import ChatbotException
from chatbot.logger import logging


def configureDataBase():
    try:
        client = MongoClient("mongodb+srv://covid19botdb:lPv7AJ5SAwqZ0iTN@cluster0.s9koz.mongodb.net/?retryWrites=true&w=majority")
        logging.info("logged into database  successfully.....")
    except Exception as e:
            raise ChatbotException(e,sys) from e
    return client.get_database('covid19db')