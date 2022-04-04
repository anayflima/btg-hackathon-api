from metrics import Metrics
import pandas as pd
import requests
from operator import itemgetter
import math
import sys
sys.path.insert(0, './')

class Portfolio:
    def __init__(self):
        pass
    
    def getFundsList(self, file):
        return pd.read_csv(file)
    
    def defineFundLiquidity(liquidityDays):
        liquidity = 0
        if (liquidityDays <= 1):
            liquidity = 3
        elif (liquidityDays <= 30):
            liquidity = 2
        else:
            liquidity = 1
        return liquidity
    
    def defineFundProfileRisk(risk):
        profile = ""
        if (risk == 1):
            profile = "Conservador"
        elif (risk == 2):
            profile = "Moderado"
        elif (risk == 3):
            profile = "Agressivo"
        return profile

    
    def calculateFundsMetrics(self, fundsList):
        fundsMetrics = []
        for i in range(len(fundsList)):
            fundMetrics = {}
            fundMetrics['fund'] = fundsList.iloc[i]['Fundo']
            fundMetrics['liquidity'] = self.defineFundLiquidity(fundsList.iloc[i]['Liquidez dias'])
            fundMetrics['liquidityDays'] = int(fundsList.iloc[i]['Liquidez dias'])
            fundMetrics['risk'] = int(fundsList.iloc[i]['Risco'])
            fundMetrics['return'] = int(fundsList.iloc[i]['Rentabilidade'])
            fundMetrics['riskProfile'] = self.defineFundProfileRisk(fundsList.iloc[i]['Risco'])
            fundMetrics['isCripto'] = fundsList.iloc[i]['Cripto']
            fundMetrics['isESG'] = fundsList.iloc[i]['ESG']
            fundsMetrics.append(fundMetrics)
        return fundsMetrics
    
    def calculateAverageMetricValue(metricValues):
        sumMetrics = sum(filter(None, metricValues))
        numberNotNone = sum(x is not None for x in metricValues)
        if (numberNotNone != 0):
            average = sumMetrics/numberNotNone
        else:
            average = sumMetrics
        return average

    def defineCustomerProfile(self, metricsUnion):
        profile = {
            'liquidity': self.calculateAverageMetricValue(metricsUnion['liquidity']),
            'risk': self.calculateAverageMetricValue(metricsUnion['risk']),
            'criptoTendency': self.calculateAverageMetricValue(metricsUnion['criptoTendency']),
        }
        return profile
    
    def transformRange(x):
        # transforms data from range 0-1 to 1-3
        return 2*x+1

    def calculateEuclideanDistance(xa,ya,xb,yb):
        return math.sqrt((xa-xb)**2 + (ya-yb)**2)

    def findBestFunds(self, customer, fundsMetrics):
        distancesFundsCustomers = {}
        funds = []

        for fund in fundsMetrics:
            customerLiquidity = float(self.transformRange(customer['liquidity']))
            customerRisk = float(self.transformRange(customer['risk']))
            euclideanDistance = self.calculateEuclideanDistance(float(fund['liquidity']), float(fund['risk']), customerLiquidity, customerRisk)
            # print("distance between (", customerLiquidity, ", ", customerRisk, ") and ", "(", float(fund['liquidity']), ", ", float(fund['risk']), ") is ", euclideanDistance)
            
            distancesFundsCustomers[fund['fund']] = euclideanDistance

            fundsInformation = {
                'fund': fund['fund'],
                'distance': euclideanDistance,
                'liquidityDays':fund['liquidityDays'],
                'riskProfile': fund['riskProfile'],
                'return': fund['return'],
            }
            funds.append(fundsInformation)
        k = 5
        bestFundsDistance = dict(sorted(distancesFundsCustomers.items(), key = itemgetter(1))[:k])
        bestFunds = []
        for fund in funds:
            if (fund['fund'] in bestFundsDistance.keys()):
                bestFunds.append(fund)

        return bestFunds
    

    def defineTotalInvestedAmount(customerId,organizationId,accountId,fromBookingDate):
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
        return sumTransactions
    
    def defineAmountToInvest(patrimony, totalAmountTransactions):
        availableAmount = patrimony - totalAmountTransactions
        return availableAmount/4
    
    def createFundsPortfolio(self, bestFunds, amountToInvest):
        distancesSum = 0
        for fund in bestFunds:
            distancesSum += fund['distance']
        positionsSum = 0
        for fund in bestFunds:
            position = (1/fund['distance'])*distancesSum
            fund['position'] = position
            positionsSum += position

        multiplicationFactor = 100/positionsSum

        for fund in bestFunds:
            fund['position'] = fund['position']*multiplicationFactor
            fund['amount'] = fund['position']*amountToInvest/100
        
        return bestFunds


    def defineCustomerPortfolio(self, customerMetricsUnion, informedPatrimony, totalAmountTransactions):
        # define customer profile
        customerProfile = self.defineCustomerProfile(self, customerMetricsUnion)

        # import and calculate funds metrics
        fundsList = self.getFundsList(self, "./btg_funds_list.csv")
        fundsMetrics = self.calculateFundsMetrics(self, fundsList)

        # quais sao os x ativos mais proximos da pessoa? distancia euclidiana em risco e liquidez - findBestFunds
        bestFunds = self.findBestFunds(self, customerProfile, fundsMetrics)

        amountToInvest = self.defineAmountToInvest(informedPatrimony, totalAmountTransactions)

        fundsPortfolio = self.createFundsPortfolio(self, bestFunds, amountToInvest)

        print(fundsPortfolio)

        customerPortfolio = {
            "portfolio": fundsPortfolio
        }

        return customerPortfolio


