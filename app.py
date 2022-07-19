#Python module Import
from flask import Flask, render_template
from flask_cors import CORS, cross_origin
import  os
import  sys

#Custom module Import
from chatbot.exception import ChatbotException
from chatbot.logger import logging
from chatbot.dialogflow_response import webhooks

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
@cross_origin()
def index():
    return render_template('index.html',)

@app.route('/results', methods=['GET','POST'])
@cross_origin()
def results():   
    a =webhooks()
    logging.info("Running Successful!!!")
    return a
    

if __name__ == '__main__':
    port = int(os.getenv('PORT'))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
    # app.run(debug=True)
