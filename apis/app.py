from flask import Flask, jsonify, request
import requests
import os
import json
import sys
sys.path.insert(0, '../models/')
from metrics import Metrics
from portfolio import Portfolio

app = Flask(__name__)

@app.route("/calculateCustomerPortfolio/<customerId>/<organizationId>")
def calculateCustomerPortfolio(customerId,organizationId):
    # pegar os dados do cliente
    customer = Metrics.getCustomerInformation(Metrics, customerId, organizationId)

    print("customer")

    print(customer)

    # chamar Metrics.calculateCustomerMetrics() com esse dados
    metricsUnion = Metrics.calculateCustomerMetrics(Metrics, customer)

    portfolio = Portfolio.defineCustomerPortfolio(Portfolio, metricsUnion)

    return portfolio


@app.route("/getAccountId/<customerId>/<organizationId>")
def getAccountIdAPI(customerId,organizationId):
    headers = {
        "customerId": customerId,
        "organizationId": organizationId,
    }
    requestUrl = "https://challenge.hackathonbtg.com/accounts/v1/accounts/"
    responseJson = requests.get(requestUrl, headers=headers)
    account = {}
    # account['accountId'] = responseJson['data'][0]['accountId']
    account['accountId'] = responseJson['data'][0]['personalId']
    return account

@app.route("/getCreditCardAccountId/<customerId>/<organizationId>")
def getCreditCardAccountIdAPI(customerId,organizationId):
    headers = {
        "customerId": customerId,
        "organizationId": organizationId,
    }
    requestUrl = "https://challenge.hackathonbtg.com/credit-cards-accounts/v1/accounts/"
    responseJson = requests.get(requestUrl, headers=headers)
    creditCard = {}
    creditCard['creditCardAccountId'] = responseJson['data'][0]['creditCardAccountId']
    return creditCard


@app.route("/getCustomerIdentification/<customerId>/<organizationId>")
def getCustomerIdentificationAPI(customerId,organizationId):
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
def getCustomerQualificationAPI(customerId,organizationId):
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

@app.route("/getAccountTransactionsAPI/<customerId>/<organizationId>/<accountId>/<fromBookingDate>")
def getAccountTransactionsAPI(customerId,organizationId,accountId,fromBookingDate):
    parameters = {
        "fromBookingDate": fromBookingDate,
    }
    headers = {
        "customerId":customerId,
        "organizationId": organizationId
    }
    requestUrl = "https://challenge.hackathonbtg.com/accounts/v1/accounts/{accountId}/transactions".format(accountId = accountId)
    response = requests.get(requestUrl, headers=headers, params = parameters)
    responseJson = response.json()
    sumTransactions = 0
    for item in responseJson['data']:
        sumTransactions += item ['amount']
    sumAccountTransactions = {
        'totalAmount': sumTransactions
    }
    return sumAccountTransactions

@app.route("/getCreditCardLimit/<customerId>/<organizationId>/<creditCardAccountId>")
def getCreditCardLimitAPI(customerId, organizationId, creditCardAccountId):
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