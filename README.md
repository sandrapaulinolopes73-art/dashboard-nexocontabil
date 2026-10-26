# Projeto de Extensão — NexoContábil (versão inicial)

## Objetivo
Demonstrar, com dados simulados, como Python, pandas e Plotly podem apoiar a análise de cobranças, pagamentos e atrasos em uma operação de administração de condomínios.

## Atenção aos dados
`dados/cobrancas_simuladas.csv` contém 300 registros **inteiramente fictícios**, criados exclusivamente para demonstração acadêmica. Não são dados reais da NexoContábil. Dados reais autorizados só devem ser adicionados depois de confirmar autorização, finalidade, minimização de dados e proteção de informações pessoais/financeiras.

## Arquivos
- `dados/cobrancas_simuladas.csv`: base simulada com 300 registros e 7 colunas.
- `app.py`: dashboard Streamlit com Plotly, dois KPIs e três gráficos.
- `requirements.txt`: bibliotecas necessárias.

## Como executar no Windows
1. Instale Python 3.11 ou uma versão compatível e o Git.
2. Extraia a pasta do projeto.
3. Abra a pasta no VS Code.
4. No terminal do VS Code, crie um ambiente virtual:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
5. Instale as bibliotecas:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Inicie o dashboard:
   ```powershell
   python -m streamlit run app.py
   ```
7. O navegador abrirá o painel. Tire capturas de tela para documentar a execução.

## Git e GitHub
Na pasta do projeto:
```powershell
git init
git add app.py requirements.txt README.md dados/cobrancas_simuladas.csv
git commit -m "Cria versão inicial do dashboard demonstrativo"
```
Depois, crie um repositório vazio no GitHub e siga as instruções exibidas pelo GitHub para adicionar o remoto e enviar os arquivos. Não envie dados reais ou documentos de autorização para um repositório público.

## Arquitetura
1. Ingestão: leitura do CSV pelo pandas.
2. Armazenamento de entrada: arquivo CSV local (base simulada).
3. Processamento: conversão e validação dos tipos de data/valor; cálculo de KPIs.
4. Visualização: dashboard Streamlit com gráficos Plotly.
5. Versionamento: Git local e GitHub, após revisão de privacidade.

## Limitações e validações necessárias
- Os nomes dos condomínios são códigos fictícios `COND-001` etc.
- O indicador de inadimplência considera cobrança com vencimento anterior à data de execução e sem data de pagamento. A regra deverá ser validada com a empresa e descrita no relatório final.
- A distribuição de status é simulada e não deve ser interpretada como taxa real da NexoContábil.
- Atualize o relatório com a problemática efetivamente confirmada, datas reais das atividades, evidências e resultados observados.
