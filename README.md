# BTG Delphos API

### Servidor

Esse repositório recebe dados da API fornecida pelo BTG Pactual:
- [Swagger Hackathon BTG](https://challenge.hackathonbtg.com/docs/#/)


A API desse repositório está hospedada no servidor:
- [BTG Delphos API](https://btg-delphos-api.herokuapp.com/)

### Descrição

Com os dados de um determinado cliente fornecidos por essa API, calcula-se o portfólio de fundos ideal para esse investidor. Para isso, estimamos a propensão ao risco do investidor e a sua necessidade de liquidez e, dessa forma, conseguimos pegar os ativos mais próximos do perfil do investidor. Quanto mais um fundo se aproximar do perfil do investidor, maior será a quantidade alocada desse fundo sugerida para ele. Os fundos foram escolhidos a partir de uma amostra de fundos do btg coletada na internet e colocada no arquivo [btg_funds_list.csv](https://github.com/anayflima/btg-hackathon-api/blob/main/btg_funds_list.csv).


### Detalhamento da estratégia de escolha da carteira do cliente 


O algoritmo contido nesse projeto se baseia em alguns dados fornecidos pela [API com dados do Open Finance](https://challenge.hackathonbtg.com/docs/#/) (os critérios que usamos são listados abaixo) para classificar o potencial de risco e necessidade de liquidez do cliente. Tendo essas métricas, podemos compará-las com características de produtos do BTG. Para exemplificar, pegamos um conjunto de fundos do BTG listados publicamente e os classificamos também em métricas de risco e liquidez. Utilizamos a classificação dada pelo site [BTG Fundos de Investimentos]( https://www.btgpactualdigital.com/fundos-de-investimento/produtos):


##### Risco

1 - Conservador
2 - Moderado
3 - Sofisticado

##### Liquidez:
1 - Resgate maior do que D+30
2 - Resgate de D+2 a D+30
3 - Resgate em D+0 ou D+1


A amostra de fundos que utilizados pode ser vista em [btg_funds_list.csv](https://github.com/anayflima/btg-hackathon-api/blob/main/btg_funds_list.csv)


Dessa forma, tendo o risco e a liquidez do cliente e dos fundos na mesma escala, calculamos os fundos mais próximos ao perfil do cliente por meio da distância euclidiana entre os produtos e o investidor, sendo a liquidez e risco os eixos x e y que usamos para calcular a distância. Selecionamos os 5 produtos com as menores distâncias euclidianas em relação ao cliente para compor o seu portfólio, sendo o tamanho da posição do fundo na carteira inversamente proporcional à sua distância euclidiana para o cliente.

#### Métricas

Para calcular as métricas do cliente, nos baseamos nas seguintes informações (o código das métricas pode ser encontrado no link: [metrics.py](https://github.com/anayflima/btg-hackathon-api/blob/main/models/metrics.py))


##### Relação entre patrimônio total e renda mensal

Esses dados foram retirados da API Customer - qualifications
A relação nos dá o número de meses que o cliente conseguiria sobreviver se não ganhasse nada e usasse toda a sua renda mensal.
Quanto maior essa relação, maior a tendência do cliente a poder estar exposto a um maior risco, já que sua reserva proporcional ao que ganha é maior e, portanto, uma maior proporção do seu patrimônio poderia ser alocada em ativos com potencial de retorno maior, mas de maior risco.


Além disso, menor tende a ser sua necessidade por liquidez, já que o dinheiro que tem guardado é maior.

##### Porcentagem que o cliente utilizou do limite de seu cartão de crédito
Esses dados foram retirados da API Credit Cards - limits
Essa porcentagem nos fornece informações sobre o quanto o cliente tende a gastar em relação ao que ele poderia (valor que teria sido calculado pelo banco ao dar ao cliente o limite).
Quanto maior essa porcentagem, maior tende a ser a necessidade do cliente por liquidez, já que ele tende a querer o dinheiro mais rapidamente para uso.


Ademais, fizemos também a função que calcula a tendência de criptoativos do cliente de acordo com a idade (análise embasada pelo artigo: [Bitcoin: pesquisa revela quem mais usa essa criptomoeda](https://ndmais.com.br/tecnologia/bitcoin-pesquisa-revela-paises-generos-e-faixas-etarias-que-mais-usam-a-criptomoeda/)). Porém, não conseguimos usar esse dado para montar a carteira, pois os dados que a API que nos foi dada devolve possuem somente pessoas nascidas em "2021-05-21".

##### Quantidade sugerida de alocação

Por fim, estimamos a quantidade que o cliente teria disponível para investir, a fim de calcular, a partir da posição do fundo na carteira, o quanto ele deveria alocar em cada ativo. Isso para facilitar o trabalho do cliente na hora de investir e escolher o quanto seria uma quantia ideal. Hoje, mesmo havendo recomendações de acordo com o perfil, não há algo automatizado que te dê a porcentagem e te sugira um valor de investimento em cada ativo. Para estimar o valor disponível do cliente para investimentos, utilizamos: 

##### Relação entre o total de transações do cliente no último mês e seu total de patrimônio
Esses dados foram retirados das APIs Accounts - transactions e Customer - qualifications
Por meio dessa relação, podemos ter uma noção do quanto de seu patrimônio é realmente movimentado pelo cliente. Calculamos o total disponível para o cliente subtraindo o seu patrimônio das transações do último mês. Selecionamos 25% desse valor para montar a carteira do cliente, já que não é boa prática investir 100% do que você tem disponível. O cliente pode escolher investir mais ou menos posteriormente.

#### Análise de dados

A fim de basear a influência desses dados e suas relações e perceber padrões, fizemos uma análise dos [dados fornecidos para o hackathon](https://btg-ob-brasa-hacks-arquivos-para-o-participante.s3.amazonaws.com/database-dump-jsons.zip). Essa análise pode ser encontrada em nosso repositório em [data_analysis.ipynb](https://github.com/anayflima/btg-hackathon-api/blob/main/data_analysis/data_analysis.ipynb).


O código dessa montagem de portfólio pode ser encontrado em: [portfolio.py](https://github.com/anayflima/btg-hackathon-api/blob/main/models/portfolio.py)

#### Próximos passos

Como um próximo passo importante para montar a carteira de investimentos do cliente, vemos o potencial uso de investimentos passados e futuros obtidos por APIs a partir da fase 4 do Open Finance. Acreditamos que isso abriria um leque ainda maior de possibilidades para medir a tendência do cliente a risco, sua necessidade de liquidez, sua tendência em investimentos de criptoativos, produtos ESG, etc.