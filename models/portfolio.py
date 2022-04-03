from models.metrics import Metric
import pandas as pd

class Portfolio:
    def __init__(self):
        self.profiles = ["Agressivo", "Moderado", "Conservador"]
    
    def calculateAverageMetricValue(metricValues):
        sumMetrics = sum(filter(None, metricValues))
        numberNotNone = sum(x is not None for x in metricValues)
        average = sumMetrics/numberNotNone
        return average
    
    def getFundsList(self, file):
        self.fundsList = pd.read_csv(file)

    def defineCustomerProfile(self, metricsUnion):
        profile = "Agressivo"
        liquidity = self.calculateAverageMetricValue(metricsUnion['liquidity'])
        risk = self.calculateAverageMetricValue(metricsUnion['risk'])
        criptoTendency = self.calculateAverageMetricValue(metricsUnion['criptoTendency'])
        # acho que nao precisa nem definir o profile - mt binario - só pegar a porcentagem e definir os ativos
        return profile


