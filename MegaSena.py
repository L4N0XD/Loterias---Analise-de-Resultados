import requests, os
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import heapq
from collections import Counter

caminho_pasta_usuario = str(os.path.expanduser('~'))
parte_especifica = r'\Documents\MegaSena'
excel_path = rf'{caminho_pasta_usuario}{parte_especifica}'

if not os.path.exists(excel_path):
    os.makedirs(excel_path)

resultados = []
listas = []

for ano in range(1996, (date.today().year + 1)):
    url = f'https://www.megasena.com/resultados/ano-{ano}'
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        linhas_tabela = soup.select('.main-results tbody tr')

        for linha in linhas_tabela:
            numero_concurso_elemento = linha.select_one('.draw-number strong a')
            data_concurso_elemento = linha.select_one('.date')
            numeros_sorteados_elementos = linha.select('.balls.-lg .ball')
            premio_principal_elemento = linha.select_one('.mobTitle')
            ganhadores = linha.select_one('td:last-child')

            if numero_concurso_elemento and data_concurso_elemento and premio_principal_elemento and numeros_sorteados_elementos:
                numero_concurso = numero_concurso_elemento.text
                data_concurso = data_concurso_elemento.text
                premio_principal = premio_principal_elemento.text
                if ganhadores:
                    ganhadores = str(ganhadores.text.strip())

                numeros_sorteados = [str(ball.text) for ball in numeros_sorteados_elementos]
                listas.append(numeros_sorteados)
                numeros_sorteados =', '.join(numeros_sorteados)

                resultado = {
                    'Número do Concurso': numero_concurso,
                    'Data do Concurso': data_concurso,
                    'Prêmio Principal': premio_principal.replace('R$ ','').replace('.', '').replace(',', '.'),
                    'Números Sorteados': numeros_sorteados,
                    'Resultado': ganhadores,
                }

                resultados.append(resultado)
        print(f"{ano} (OK)")
    else:
        print(f"{ano} (ERRO NA REQUISIÇÃO: {response.status_code})")
    

resultados = sorted(resultados, key=lambda x: int(x['Número do Concurso'].split()[-1]))

for resultado in resultados:
    print(f"Número do Concurso: {resultado['Número do Concurso']}")
    print(f"Data do Concurso: {resultado['Data do Concurso']}")
    print(f"Prêmio Principal: {resultado['Prêmio Principal']}")
    print(f"Números Sorteados: {resultado['Números Sorteados']}")
    print(f"Resultado: {resultado['Resultado']}")
    print("\n")

df = pd.DataFrame(resultados)
with pd.ExcelWriter(rf'{excel_path}\MegaSena.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name="MegaSena", index=False)
    for sheet in writer.sheets.values():
        for col in sheet.columns:
            sheet.auto_filter.ref = sheet.dimensions
            max_length = 0
            column = col[0].column_letter  
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value) + 1
                except:
                    pass
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[column].width = adjusted_width
print("Dados salvos com sucesso no arquivo MegaSena.xlsx")

df['Data do Concurso'] = pd.to_datetime(df['Data do Concurso'], format='%d/%m/%Y')

df['Prêmio Principal'] = pd.to_numeric(df['Prêmio Principal'], errors='coerce')

diferenca_datas = df['Data do Concurso'].diff().mean()
ultima_data = pd.to_datetime(df['Data do Concurso'].max())  # Convert to datetime

concurso_14_data = ultima_data + diferenca_datas
concurso_14_numero = int(str(df['Número do Concurso'].max()).replace("Concurso ", '')) + 1

# Calculando a próxima estimativa de valor
diferenca_valores = df['Prêmio Principal'].diff().mean()
ultimo_valor = df['Prêmio Principal'].iloc[-1]

concurso_14_valor = ultimo_valor + diferenca_valores

# Formatando a data para o mesmo formato da planilha
concurso_14_data_str = concurso_14_data.strftime('%d/%m/%Y')

#print(f'Concurso {concurso_14_numero} - Data: {concurso_14_data_str}, Valor: R${concurso_14_valor:.2f}')


todos_numeros = [numero for lista in listas for numero in lista]
total_numeros = len(todos_numeros)
frequencia_numeros = Counter(todos_numeros)
medias_numeros = {str(num): sum(i + 1 for i, lista in enumerate(listas) if num in lista) / len(listas) for num in todos_numeros}
numeros_mais_frequentes = heapq.nlargest(6, frequencia_numeros, key=frequencia_numeros.get)
numeros_menos_frequentes = heapq.nsmallest(6, frequencia_numeros, key=frequencia_numeros.get)
numeros_mais_provaveis = heapq.nsmallest(6, medias_numeros, key=medias_numeros.get)
numeros_menos_provaveis = heapq.nlargest(6, medias_numeros, key=medias_numeros.get)


print("Os 6 números mais prováveis de caírem são:", sorted(numeros_mais_provaveis, key=lambda x: int(x)))
print("Os 6 números menos prováveis de caírem são:", sorted(numeros_menos_provaveis, key=lambda x: int(x)))
print("Os 6 números que mais se repetem são:", sorted(numeros_mais_frequentes, key=lambda x: int(x)))
print("Os 6 números que menos se repetem são:", sorted(numeros_menos_frequentes, key=lambda x: int(x)))


