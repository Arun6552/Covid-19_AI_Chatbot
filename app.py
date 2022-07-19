#Python module Import
from flask import Flask, render_template
from flask_cors import CORS, cross_origin
import  os
import  sys

#Custom module Import
<<<<<<< HEAD
from chatbot.exception import ChatbotException
from chatbot.logger import logging
from chatbot.dialogflow_response import webhooks
=======
# from chatbot.exception import ChatbotException
# from chatbot.logger import logging
# from chatbot.api_request import Api
# from chatbot.dialogflow_response import webhooks
>>>>>>> 18f24486170eb45a5ba1b436053f424b87acf623

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
@cross_origin()
def index():
    return render_template('index.html',)

<<<<<<< HEAD
@app.route('/results', methods=['GET','POST'])
@cross_origin()
def results():   
    a =webhooks()
    logging.info("Running Successful!!!")
    return a
    

if __name__ == '__main__':
    # port = int(os.getenv('PORT'))
    # print("Starting app on port %d" % port)
    # app.run(debug=False, port=port, host='0.0.0.0')
    app.run(debug=True)
=======
# @app.route('/results', methods=['GET','POST'])
# @cross_origin()
# def results():   
#     a =webhooks()
#     # logging.info("Running Successful!!!")
#     return a
    

if __name__ == '__main__':
    port = int(os.getenv('PORT'))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
    # app.run(debug=True)
>>>>>>> 18f24486170eb45a5ba1b436053f424b87acf623
