from flask import Flask, jsonify, request
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

@app.route("/calculateCustomerPortfolio/<customerId>/<organizationId>")
def calculateCustomerPortfolio(customerId,organizationId):
    # pegar os dados do cliente
    customer = Metrics.getCustomerInformation(Metrics, customerId, organizationId)

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