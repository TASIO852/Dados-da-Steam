# Projeto: Engenharia de Dados da Steam

Este projeto consiste na extração, armazenamento relacionados às vendas do site SteamDB. A seguir, detalharemos as etapas envolvidas no processo.

## Como o projeto funciona

1. **Extração de dados da web**: Começamos com um script Python que realiza uma solicitação HTTP à página [SteamDB](https://steamdb.info/sales/). O script raspa os dados contidos na tabela de vendas.
![Alt text](Docs/img/api_settings.png)
2. **Armazenamento dos dados no Google BigQuery**: A próxima etapa envolve armazenar os dados extraídos no Google BigQuery. O processo começa com a criação de um projeto no Google Cloud, seguido pela configuração de um conjunto de dados e uma tabela correspondente no BigQuery para acomodar os dados.É importante ressaltar que para se comunicar com o Google BigQuery, é necessária uma chave de autenticação em formato JSON, fornecida pelo Google Cloud. Essa chave deve ser armazenada em um local seguro em seu ambiente local e seu caminho deve ser definido na variável de ambiente 'GOOGLE_APPLICATION_CREDENTIALS'.
![Alt text](Docs/img/bigquery_print.png)
3. **Conexão dos dados com o Google Sheets**: O último passo envolve conectar os dados do BigQuery ao Google Sheets. Através da funcionalidade "Conectar-se ao BigQuery", disponível no Google Sheets, é possível realizar consultas SQL no BigQuery diretamente no Google Sheets e importar os resultados para a planilha desejada.
![Alt text](Docs/img/google_sheets.png)

## Considerações Futuras

Embora o projeto esteja funcional, ele poderia ser aprimorado com mais tempo e recursos. Algumas possibilidades de aprimoramentos incluem:

1. Implementação de um processo de Integração Contínua/Entrega Contínua (CI/CD) utilizando GitHub Actions.
2. Aumento da segurança do projeto através da ocultação do arquivo `headers.py ea chave de usuario do GCP` com o uso do GitHub Secrets.
3. Automatização do processo e implantação no Google Cloud Platform (GCP), utilizando serviços como o Cloud Functions e o Cloud Storage.
4. Utilização de Infraestrutura como Código (IaC) com o Terraform para gerenciar os custos da infraestrutura no GCP e ter maior controle sobre os recursos utilizados.

## Arquitetura do Pipeline

A seguinte imagem ilustra como seria a arquitetura do pipeline após a implementação das melhorias propostas:

![Arquitetura do Pipeline](Docs/img/arquitetura.png)

Para ter uma estimativa dos custos associados a esta arquitetura, acesse o seguinte link: [Estimativa de Custo](<Docs/Calculadora de preços do Google Cloud.pdf>).
