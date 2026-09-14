# Titanic - Dashboard de Analise Interativa

## Acesso Online
O dashboard esta hospedado e funcionando na nuvem. Voce pode visualizar e interagir com o projeto diretamente pelo navegador acessando o link abaixo, sem a necessidade de baixar o codigo ou instalar dependencias:
https://titanic-challenge-f5fbaesxzbvwdjvmrcgxm7.streamlit.app/

## Sobre este Projeto e o Uso de IA
Este projeto foi desenvolvido com um proposito estritamente educativo. Ele marca a minha primeira experiencia construindo uma aplicacao em colaboracao direta com um agente de Inteligencia Artificial, o opencode MiMo. O objetivo principal foi aprender na pratica como interagir com IAs para desenvolver software, construir interfaces web, manipular dados e versionar codigo de forma eficiente.

## O que o Dashboard Mostra
O dashboard e uma interface visual interativa que explora o famoso dataset do desafio do Titanic (Kaggle). Funcionalidades principais:
- Filtros dinamicos de passageiros (por genero, classe e porto de embarque).
- Exibicao de metricas gerais (taxa de sobrevivencia, total de passageiros, etc.).
- Graficos para analise de distribuicao de dados e perfis de sobrevivencia.

> Adendo sobre a coluna de Idades: 
> Na tabela e nos graficos, algumas idades aparecem com casas decimais ou virgulas (ex: 0.42 ou 32.5). Optei por deixar esses numeros exatamente como vieram na base de dados original do Kaggle, sem aplicar tratamentos de arredondamento. No contexto do dataset, fracoes indicam bebes com menos de 1 ano ou idades estimadas na epoca, portanto, os dados brutos foram mantidos fieis a fonte.

## Ferramentas Utilizadas
- Ambiente de Desenvolvimento: VSCode
- Linguagem: Python
- Bibliotecas: Streamlit (Interface Web), Pandas (Manipulacao de Dados) e Plotly (Graficos Interativos)
- Controle de Versao: Git e GitHub
- Assistente de IA: opencode MiMo

## Como Executar o Projeto Localmente
1. Certifique-se de ter o Python instalado.
2. Instale as bibliotecas necessarias:
   ```bash
   pip install streamlit pandas plotly
   ```
3. Execute o dashboard:
   ```bash
   streamlit run app.py
   ```
