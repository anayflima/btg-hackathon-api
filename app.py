from flask import Flask, jsonify, request
import requests
import os
import json
import sys
sys.path.insert(0, './models/')
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