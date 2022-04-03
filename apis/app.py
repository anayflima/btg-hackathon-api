from flask import Flask, jsonify, request
import requests
import os
import urllib.request


app = Flask(__name__)

@app.route("/getCustomerQualification/<customerId>/<organizationId>")
def getCustomerQualification(customerId,organizationId):
    headers = {
        'accept': 'application/json',
        "customerId": customerId,
        "organizationId": organizationId,
    }
    requestUrl = "https://challenge.hackathonbtg.com/customers/v1/personal/qualifications"
    print(requestUrl)
    # response = requests.get(requestUrl, headers = headers)
    req = urllib.request.Request(url=requestUrl,headers = headers)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    print("RESPONSE HEADERS = ", req.headers)
    print("RESPONSE = ", the_page)
    return the_page

@app.route("/getAccountTransactions/<customerId>/<organizationId>/<accountId>/<fromBookingDate>")
def getAccountTransactions(customerId,organizationId,accountId,fromBookingDate):
    parameters = {
        "fromBookingDate": fromBookingDate,
    }
    headers = {
        "customerId": customerId,
        "organizationId": organizationId,
    }
    requestUrl = "https://challenge.hackathonbtg.com/accounts/v1/accounts/{accountId}/transactions".format(accountId = accountId)
    print(requestUrl)
    response = requests.get(requestUrl, headers = headers, params = parameters)
    print("RESPONSE HEADERS = ", response.headers)
    print("RESPONSE = ", response.json())
    return response.json()

@app.route("/defineCustomerProfile")
def defineCustomerProfile():
    title = request.json["title"]
    body = request.json["body"]

    return jsonify({"title": title, "body": body})

if __name__ == "__main__":
    # app.run(debug = True)
    app.run()