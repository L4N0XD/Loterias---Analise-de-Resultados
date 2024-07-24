#  Loterias - Análise de Resultados

## Visão Geral

Este script em Python realiza as seguintes tarefas:

1. **Extração de Dados das Loterias**:
   - Itera pelos anos de início até o ano atual.
   - Para cada ano, busca os resultados dos concursos.

2. **Armazenamento dos Resultados**:
   - Para cada resultado válido encontrado, os dados são estruturados em um dicionário e adicionados à lista `resultados`.
   - Os dados incluem número do concurso, data, prêmio principal, números sorteados e quantidade de ganhadores.

3. **Geração do Arquivo Excel**:
   - Os resultados são organizados em um DataFrame do Pandas.
   - Um arquivo Excel é criado na pasta específica do usuário.
   - Cada coluna no arquivo Excel é ajustada para uma largura máxima apropriada para garantir que todos os dados sejam visíveis.

4. **Análise dos Números Sorteados**:
   - Todos os números sorteados são coletados em uma lista.
   - Calcula-se a frequência de cada número usando `Counter` da biblioteca `collections`.
   - Calcula-se a média de ocorrências de cada número ao longo dos concursos.
   - Identifica os números mais e menos prováveis de serem sorteados, bem como os números que mais e menos se repetiram.

### Exemplo de Saída:
- O script imprime os números mais prováveis de serem sorteados, os menos prováveis, os mais frequentes e os menos frequentes.

```plaintext
Os 6 números mais prováveis de caírem são: ['10', '21', '22', '35', '37', '43']
Os 6 números menos prováveis de caírem são: ['06', '15', '29', '30', '34', '39']
Os 6 números que mais se repetem são: ['05', '33', '42', '43', '51', '53']
Os 6 números que menos se repetem são: ['04', '07', '12', '14', '16', '18']
