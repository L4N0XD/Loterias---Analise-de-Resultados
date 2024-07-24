import requests, os
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import heapq
from collections import Counter

caminho_pasta_usuario = str(os.path.expanduser('~'))
parte_especifica = r'\Documents\LotoFacil'
excel_path = rf'{caminho_pasta_usuario}{parte_especifica}'

if not os.path.exists(excel_path):
    os.makedirs(excel_path)

resultados = []
listas = []

for concurso in range(1, 2994):
    url = f'https://www.intersena.com.br/lotofacil/resultados/{concurso}'
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        elemento_sorteio = soup.find('div', class_='resultado-individual-sorteio')

        # Verificar se o elemento foi encontrado
        if elemento_sorteio:
            # Encontrar todos os elementos com a classe resultado-individual-numero-sorteado dentro do elemento_sorteio
            numeros_sorteados_elementos = elemento_sorteio.find_all('span', class_='resultado-individual-numero-sorteado bg-color-lotofacil')
            date_element = soup.find('h2', class_='text-lotofacil')
            numeros_sorteados = [elemento.text for elemento in numeros_sorteados_elementos]
            data_concurso = date_element.text.strip().split(", ")[1]

            # Exibir os resultados
            listas.append(numeros_sorteados)
            numeros_sorteados = ','.join(numeros_sorteados)
            numeros_sorteados = str(numeros_sorteados).replace(' ', '')
            print('Números Sorteados:', (numeros_sorteados))

            resultado = {
                'Número do Concurso': str(concurso),
                'Data do Concurso': data_concurso,
                'Números Sorteados': numeros_sorteados,
            }

            resultados.append(resultado)
    else:
        print(f"Concurso: {concurso} (ERRO NA REQUISIÇÃO: {response.status_code})")
    

resultados = sorted(resultados, key=lambda x: int(x['Número do Concurso'].split()[-1]))

df = pd.DataFrame(resultados)
with pd.ExcelWriter(rf'{excel_path}\LotoFacil.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name="LotoFacil", index=False)
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
print("Dados salvos com sucesso no arquivo LotoFacil.xlsx")

df['Data do Concurso'] = pd.to_datetime(df['Data do Concurso'], format='%d/%m/%Y')


todos_numeros = [numero for lista in listas for numero in lista]
total_numeros = len(todos_numeros)
frequencia_numeros = Counter(todos_numeros)
medias_numeros = {str(num): sum(i + 1 for i, lista in enumerate(listas) if num in lista) / len(listas) for num in todos_numeros}
numeros_mais_frequentes = heapq.nlargest(15, frequencia_numeros, key=frequencia_numeros.get)
numeros_menos_frequentes = heapq.nsmallest(15, frequencia_numeros, key=frequencia_numeros.get)
numeros_mais_provaveis = heapq.nsmallest(15, medias_numeros, key=medias_numeros.get)
numeros_menos_provaveis = heapq.nlargest(15, medias_numeros, key=medias_numeros.get)


print("Os 15 números mais prováveis de caírem são:", ','.join(sorted(numeros_mais_provaveis, key=lambda x: int(x))))
print("Os 15 números menos prováveis de caírem são:", ','.join(sorted(numeros_menos_provaveis, key=lambda x: int(x))))
print("Os 15 números que mais se repetem são:", ','.join(sorted(numeros_mais_frequentes, key=lambda x: int(x))))
print("Os 15 números que menos se repetem são:", ','.join(sorted(numeros_menos_frequentes, key=lambda x: int(x))))


