import numpy as np

class Metrics:
    def __init__(self):
        pass
    def calculateAgeImpact(self, ageInfo):
        age = ageInfo['age']
        metrics = {
            'risk': None,
            'liquidity': None,
            'criptoTendency': None
        }

        # age between 25 and 34 years -> 46,3% have interesse in cryptocurrencies
        # age between 35 and 44 years -> 26,8% have interesse in cryptocurrencies
        # age between 18 and 24 years or 45 and 54 -> 10,3% have interesse in cryptocurrencies
        # source: https://ndmais.com.br/tecnologia/bitcoin-pesquisa-revela-paises-generos-e-faixas-etarias-que-mais-usam-a-criptomoeda/

        if (25 <= age <= 34):
            metrics['criptoTendency'] = 0.463
        elif (35 <= age <= 44):
            metrics['criptoTendency'] = 0.268
        elif (18 <= age <= 24):
            metrics['criptoTendency'] = 0.103

        metrics['risk'] = (100-age)/200

        return metrics
    
    def calculateSigmoid(x):
        return 1/(1+np.exp(-(1/x)))
    
    def calculatePatrimonyOnIncomeImpact(self, qualificationInfo):
        patrimony = qualificationInfo['patrimony']
        income = qualificationInfo['income']
        metrics = {
            'risk': None,
            'liquidity': None,
            'criptoTendency': None
        }
        patrimonyOnIncome = patrimony/income
        
        # The higher the proportion of patrimony in relation to mensal income,
        # the lower the need to high liquidity
        
        # In order to normalize the liquidity metric between 0 and 1, we use the sigmoid function
        # As the sigmoid function has a sharp curve, it's a good function to represent
        # liquidity, since we'll use this value to recommend funds with liquidity
        # classified with integer values between 1 and 3
        
        metrics['liquidity'] = (self.calculateSigmoid(patrimonyOnIncome)-0.5)*2
            
        
        print(metrics['liquidity'])
        # The higher the proportion of patrimony in relation to mensal income,
        # the higher the tendency to be able to be exposed to greater risk
        
        metrics['risk'] = 1-(self.calculateSigmoid(patrimonyOnIncome)-0.5)*2
        
        print(metrics['risk'])
        
        return metrics

    def calculateCreditLimitImpact(self, limitInfo):
        limitAmount = limitInfo['limitAmount']
        usedAmount = limitInfo['usedAmount']
        
        metrics = {
            'risk': None,
            'liquidity': None,
            'criptoTendency': None
        }
        
        usedAmountPercentage = usedAmount/limitAmount
        
        # The more the customer used his card limit, the more he needs liquidity, as he tends to want the money faster to use
        
        metrics['liquidity'] = usedAmountPercentage
        
        return metrics
    
    def appendMetrics(self, metricsUnion, calculateImpact, **kwargs):
        metrics = calculateImpact(self, kwargs)
        for key in metricsUnion.keys():
            if (key in metrics):
                metricsUnion[key].append(metrics[key])
        return metricsUnion

    def calculateAllMetrics(self, age, patrimony, income, limitAmount, usedAmount):
        metricsUnion = {
            'risk': [],
            'liquidity': [],
            'criptoTendency': [],
        }
        
        self.appendMetrics(self, metricsUnion,self.calculateAgeImpact, age = age)
        self.appendMetrics(self, metricsUnion,self.calculateCreditLimitImpact, limitAmount = limitAmount, usedAmount = usedAmount)
        self.appendMetrics(self, metricsUnion,self.calculatePatrimonyOnIncomeImpact, patrimony = patrimony, income = income)
        
        return metricsUnion