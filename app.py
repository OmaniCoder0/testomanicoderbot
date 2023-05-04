from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
from pymongo import MongoClient
from datetime import datetime
import urllib.parse

username = urllib.parse.quote_plus("Omanicoder")
password = urllib.parse.quote_plus("A4,s!kap@mvso62")
cluster = MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.zg6btbc.mongodb.net/OmaniCoder?retryWrites=true&w=majority")
db = cluster["OmaniCoder"]
users = db["users"]
orders = db["orders"]
app = Flask(__name__)
@app.route("/", methods=["get", "post"])

def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")[:-2]
    response = MessagingResponse()
    # check if user is new
    message = Message()
    user = users.find_one({"number": number})
    if user is None:
        # user is new, send welcome message

        response.message("Welcome to Omani Coder WhatsApp chatbot🤖")
        response.message("\n 1. Services: \n 2. Prices: \n 3. contact numbers:\n 4. sign in:")
        users.insert_one({"number": number, "status": "main", "messages": []})
        return str(response)

        return str(response)
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            response.message("Please enter a valid response")
            return str(response)

        if option == 1:
            response.message("You have entered services page")
            response.message("Please select one of our services:\n 1. WhatsApp chatbot\n 2. Instagram API \n 3. Website chatbot\n 0. to go back")
            users.update_one({"number": number}, {"$set": {"status": "services"}})
        elif option == 2:
            response.message("Please type in the number of messages the bot can send for your business:")
            users.update_one({"number": number}, {"$set": {"status": "prices"}})
        elif option == 3:
            response.message("email: coderomani@gmail.com\n WhatsApp: 91262005")
        elif option == 4:
            response.message(" type your email to sign in")
        else:
            response.message("Please enter a valid response")
    elif user["status"] == "services":
        try:
            option = int(text)
        except:
            response.message("Please enter a valid response")
            return str(response)
        if option == 0:
            response.message("Returning to main menu...")
            response.message("\n 1. Services: \n 2. Prices: \n 3. contact numbers:\n 4. sign in:")
            users.update_one({"number": number}, {"$set": {"status": "main"}})
        else:
            response.message("You have selected option {}.".format(option))
    elif user["status"] == "prices":
        response.message("You have entered {} messages.".format(text))
        users.update_one({"number": number}, {"$set": {"status": "main"}})

    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})

    return str(response)
    
if __name__ == "__main__":
    # Debug/Development
    app.run()
    # Production
