class Metrics:
    def __init__(self):
        pass
    def calculateAgeImpact(ageInfo):
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

        metrics['risk'] = (100-age)/2

        return metrics
    
    def calculatePatrimonyOnIncomeImpact(qualificationInfo):
        patrimony = qualificationInfo['patrimony']
        income = qualificationInfo['income']
        metrics = {
            'risk': None,
            'liquidity': None,
            'criptoTendency': None
        }
        patrimonyOnIncome = patrimony/income
        
        # The bigger the proportion of patrimony in relation to mensal income,
        # the lower the need to high liquidity]
        
        if (patrimonyOnIncome != 0):
            metrics['liquidity'] = 1/patrimonyOnIncome
        
        # The bigger the proportion of patrimony in relation to mensal income,
        # the bigger the tendency to be exposed to greater risk
        
        risk = -(1 - patrimonyOnIncome)/patrimonyOnIncome # MUDARRRRR
        # normalize between 0 and 1
        metrics['risk'] = (risk - 0)/1
        
        return metrics

    def calculateCreditLimitImpact(limitInfo):
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
    
    def appendMetrics(metricsUnion, calculateImpact, **kwargs):
        metrics = calculateImpact(kwargs)
        for key in metricsUnion.keys():
            if (key in metrics):
                metricsUnion[key].append(metrics[key])
        return metricsUnion

    def callAllMetrics(self, age, patrimony, income, limitAmount, usedAmount):
        metricsUnion = {
            'risk': [],
            'liquidity': [],
            'criptoTendency': [],
        }
        
        self.appendMetrics(metricsUnion,self.calculateAgeImpact, age = age)
        self.appendMetrics(metricsUnion,self.calculateCreditLimitImpact, limitAmount = limitAmount, usedAmount = usedAmount)
        self.appendMetrics(metricsUnion,self.calculatePatrimonyOnIncomeImpact, patrimony = patrimony, income = income)
        
        return metricsUnion

    def testCase():
        return Metrics.callAllMetrics(Metrics,18, 1000, 100, 300, 150)