from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import json
import sys
sys.path.insert(0, './models/')
from metrics import Metrics
from portfolio import Portfolio
import datetime
import dateutil.relativedelta

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/calculateCustomerPortfolio/<customerId>/<organizationId>")
def calculateCustomerPortfolio(customerId,organizationId):
    # pegar os dados do cliente
    # customer = Metrics.getCustomerInformation(Metrics, customerId, organizationId)

    # como a API com os dados do cliente ficou indisponível após o término do hackathon,
    # vamos colocar os dados de um determinado cliente (o de CPF 595.080.896-84) 
    # do banco de dados para podermos rodar a construção do portfólio

    customer = {}
        
    # accountId
    customer['accountId'] = "dc728105-74a5-47fe-b18c-23a6c855ed30"
    
    # creditCardAccountId
    customer['creditCardAccountId'] = "0b899b56-2f36-46c4-a594-b2a921f45575"
    
    # age
    customer['age'] = 1
    
    # customerQualification
    customer['informedIncome'] = 4894.45
    customer['informedPatrimony'] = 29653.89
    
    # creditCardInformation
    customer['limitAmount'] = 14446.89
    customer['usedAmount'] = 8490.13

    print("customer")

    print(customer)

    # chamar Metrics.calculateCustomerMetrics() com esse dados
    metricsUnion = Metrics.calculateCustomerMetrics(Metrics, customer)

    now = datetime.datetime.now()
    
    fromBookingDate = (now + dateutil.relativedelta.relativedelta(months=-1)).strftime("%Y-%m-%d")

    totalAmountTransactions = Portfolio.defineTotalInvestedAmount(customerId,
        organizationId,customer['accountId'],fromBookingDate)

    portfolio = Portfolio.defineCustomerPortfolio(Portfolio, metricsUnion,
            customer['informedPatrimony'], totalAmountTransactions)

    return portfolio