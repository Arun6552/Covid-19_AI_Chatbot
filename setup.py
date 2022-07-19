from setuptools import setup,find_packages
from typing import List


## Declearing variables for setup functions
PROJECT_NAME = 'covid-19_AI_Chatbot'
VERSION = "0.0.1"
AUTHOR = "ARUN CHAUDHARY"
DESCRIPTION = "It is an AI Chat bot which helps the user to get the Covid-19 related information. It will Show statisics based on Country,Indian States,Indian districts,Google Maps,WorldWide data related to covid-19."
PACKAGES = ['chatbot']
REQUIREMENT_FILE_NAME = "requirements.txt"



def get_requirements_list()->List[str]:
    """"
    Description : This function is going to return list of the requirements mention 
    in requirements.txt file
    return : This function is going to return a list which contains name of the libaries mentioned in the requirements.txt file
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        # return requirement_file.readlines()
        return requirement_file.readlines().remove("-e .")





setup(
    name = PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description= DESCRIPTION,
    # packages=PACKAGES,
    packages=find_packages(),
    install_requires = get_requirements_list(),


)