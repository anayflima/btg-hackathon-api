from flask import Flask, jsonify, request
import requests
import os
import json


app = Flask(__name__)


@app.route("/getCustomerIdentification/<customerId>/<organizationId>")
def getCustomerIdentification(customerId,organizationId):
    headers = {
        "customerId": customerId,
        "organizationId": organizationId,
    }
    requestUrl = "https://challenge.hackathonbtg.com/customers/v1/personal/identifications"
    responseJson = requests.get(requestUrl, headers=headers)
    customerIdentification = {}
    customerIdentification['age'] = responseJson['data']['birthDate']
    return customerIdentification

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
    responseJson = response.json()
    customerQualification = {}
    customerQualification['informedIncome'] = responseJson["data"]["informedIncome"]["amount"]
    customerQualification['informedPatrimony'] = responseJson["data"]["informedPatrimony"]["amount"]
    return customerQualification

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

@app.route("/getCreditCardLimit/<customerId>/<organizationId>/<creditCardAccountId>")
def defineCustomerProfile(customerId, organizationId, creditCardAccountId):
    headers = {
        "accept": "application/json",
        "customerId": customerId,
        "organizationId": organizationId,
    }
    requestUrl = "https://challenge.hackathonbtg.com/credit-cards-accounts/v1/accounts/{creditCardAccountId}/limits".format(creditCardAccountId = creditCardAccountId)
    response = requests.get(requestUrl, headers=headers)
    responseJson = response.json()
    print(responseJson)
    creditCardLimit = {
        'limitAmount': 0,
        'usedAmount': 0
    }
    for limit in responseJson["data"]:
        creditCardLimit['limitAmount'] += limit["limitAmount"]
        creditCardLimit['usedAmount'] += limit["usedAmount"]
    
    return creditCardLimit

if __name__ == "__main__":
    # app.run(debug = True)
    app.run()