from metrics import Metrics
import pandas as pd
from operator import itemgetter
import math

class Portfolio:
    def __init__(self):
        pass
    
    def getFundsList(self, file):
        self.fundsList = pd.read_csv(file)
    
    def defineFundLiquidity(liquidityDays):
        liquidity = 0
        if (liquidityDays <= 1):
            liquidity = 3
        elif (liquidityDays <= 30):
            liquidity = 2
        else:
            liquidity = 1
        return liquidity
    
    def calculateFundsMetrics(self):
        fundsMetrics = []
        for i in range(len(self.fundsList)):
            fundMetrics = {}
            fundMetrics['fund'] = self.fundsList.iloc[i]['Fundo']
            fundMetrics['liquidity'] = self.defineFundLiquidity(self.fundsList.iloc[i]['Liquidez dias'])
            fundMetrics['risk'] = self.fundsList.iloc[i]['Risco']
            fundMetrics['isCripto'] = self.fundsList.iloc[i]['Cripto']
            fundMetrics['isESG'] = self.fundsList.iloc[i]['ESG']
            fundsMetrics.append(fundMetrics)
    
    def calculateAverageMetricValue(metricValues):
        sumMetrics = sum(filter(None, metricValues))
        numberNotNone = sum(x is not None for x in metricValues)
        average = sumMetrics/numberNotNone
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
        fundsPortfolio = dict(sorted(distancesFundsCustomers.items(), key = itemgetter(1))[:k])
        return fundsPortfolio

    def defineCustomerPortfolio(profile, fundsMetrics):
        pass

    def testCase():
        # pegar os dados do cliente

        # chamar Metrics.calculateAllMetrics() com esse dados

        # calcular perfil - defineCustomerProfile

        # importar e calcular metricas do fundo - calculateFundsMetrics

        # quais sao os x ativos mais proximos da pessoa? distancia euclidiana em risco e liquidez - findBestFunds

        # dependendo da tendencia cripto, colocar um pouco em crito
        return 
    
    testCase()


