from flask import Flask, jsonify, request
import requests
import os
import json


app = Flask(__name__)

@app.route("/getCustomerQualification/<customerId>/<organizationId>")
def getCustomerQualification(customerId,organizationId):
    headers = {
        "accept": "application/json",
        "customerId": customerId,
        "organizationId": organizationId,
    }
    requestUrl = "https://challenge.hackathonbtg.com/customers/v1/personal/qualifications"
    print(requestUrl)
    response = requests.get(requestUrl, headers = headers)
    return response.json()

@app.route("/getAccountTransactions/<customerId>/<organizationId>/<accountId>/<fromBookingDate>")
def getAccountTransactions(customerId,organizationId,accountId,fromBookingDate):
    parameters = {
        "fromBookingDate": fromBookingDate,
    }
    headers = {
        "customerId":customerId,
        "organizationId": organizationId
    }
    requestUrl = "https://challenge.hackathonbtg.com/accounts/v1/accounts/{accountId}/transactions".format(accountId = accountId)
    response = requests.get(requestUrl, headers=headers, params = parameters)

    return response.json()

@app.route("/getCustomerIdentification/<customerId>/<organizationId>")
def getCustomerIdentification(customerId,organizationId):
    headers = {
        "customerId": customerId,
        "organizationId": organizationId,
    }
    requestUrl = "https://challenge.hackathonbtg.com/customers/v1/personal/identifications"
    response = requests.get(requestUrl, headers=headers)
    return response.json()
    

@app.route("/defineCustomerProfile")
def defineCustomerProfile():
    title = request.json["title"]
    body = request.json["body"]

    return jsonify({"title": title, "body": body})

if __name__ == "__main__":
    # app.run(debug = True)
    app.run()