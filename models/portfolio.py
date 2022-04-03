from metrics import Metrics
import pandas as pd
from operator import itemgetter
import math

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
    
    def calculateFundsMetrics(self, fundsList):
        fundsMetrics = []
        for i in range(len(fundsList)):
            fundMetrics = {}
            fundMetrics['fund'] = fundsList.iloc[i]['Fundo']
            fundMetrics['liquidity'] = self.defineFundLiquidity(fundsList.iloc[i]['Liquidez dias'])
            fundMetrics['risk'] = fundsList.iloc[i]['Risco']
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

        for fund in fundsMetrics:
            customerLiquidity = float(self.transformRange(customer['liquidity']))
            customerRisk = float(self.transformRange(customer['risk']))
            euclideanDistance = self.calculateEuclideanDistance(float(fund['liquidity']), float(fund['risk']), customerLiquidity, customerRisk)
            # print("distance between (", customerLiquidity, ", ", customerRisk, ") and ", "(", float(fund['liquidity']), ", ", float(fund['risk']), ") is ", euclideanDistance)
            distancesFundsCustomers[fund['fund']] = euclideanDistance
        k = 5
        bestFunds = dict(sorted(distancesFundsCustomers.items(), key = itemgetter(1))[:k])
        return bestFunds
    
    def createFundsPortfolio(self, bestFunds):
        portfolio = []

        distancesSum = sum(bestFunds.values())
        positionsSum = 0
        for key in bestFunds.keys():
            fund = {
                'fund': key,
            }
            position = (1/bestFunds[key])*distancesSum
            fund['position'] = position
            positionsSum += position
            portfolio.append(fund)

        multiplicationFactor = 100/positionsSum

        for fund in portfolio:
            fund['position'] = fund['position']*multiplicationFactor
        
        return portfolio

    def defineCustomerPortfolio(self, customerMetricsUnion):
        # define customer profile
        customerProfile = self.defineCustomerProfile(self, customerMetricsUnion)

        # import and calculate funds metrics
        fundsList = self.getFundsList(self, "../data/btg_funds_list.csv")
        fundsMetrics = self.calculateFundsMetrics(self, fundsList)

        # quais sao os x ativos mais proximos da pessoa? distancia euclidiana em risco e liquidez - findBestFunds
        bestFunds = self.findBestFunds(self, customerProfile, fundsMetrics)

        fundsPortfolio = self.createFundsPortfolio(self, bestFunds)

        print(type(fundsPortfolio))

        customerPortfolio = {
            "portfolio": fundsPortfolio
        }

        return customerPortfolio


