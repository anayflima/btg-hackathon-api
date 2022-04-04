# BTG Delphos API

### Servidor

Esse repositório recebe dados da API fornecida pelo BTG Pactual:
- [Swagger Hackathon BTG](https://challenge.hackathonbtg.com/docs/#/)

Com esses dados, calcula-se o portfólio de fundos ideal para o investidor. Foi usada uma amostra de fundos coletadas na internet e colocada no arquivo btg_funds_list.csv. Com esses dados, estimamos a propensão ao risco do investidor e a sua necessidade de liquidez. Dessa forma, conseguimos pegar os ativos mais próximos do perfil do investidor. Quanto mais o fundo se aproximar do perfil do investidor, maior será a quantidade alocada sugerida para ele.

A API desse repositório está hospedada no servidor:
- [BTG Delphos API](https://btg-delphos-api.herokuapp.com/)