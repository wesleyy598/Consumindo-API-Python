import http.client
import csv
import json

def fetch_items_page(page):
    conn = http.client.HTTPSConnection("empresa.app.invoicexpress.com")
    headers = {'accept': "application/json"}
    conn.request("GET", f"/items.json?page={page}&per_page=30&api_key=sua-api-key-aqui", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data)

# Especificando o nome do arquivo CSV de saída
output_csv_file = "output_all_items.csv"

# Abrindo o arquivo CSV em modo de escrita
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
    # Criando um objeto de gravação CSV com ponto e vírgula como delimitador
    csv_writer = csv.writer(csvfile, delimiter=';')

    # Escrevendo o cabeçalho do CSV
    csv_writer.writerow(["name", "description", "unit_price", "unit", "tax_name"])

    total_pages = 42  # Atualize esse valor com o número real de páginas
    
    for page in range(1, total_pages + 1):
        response_json = fetch_items_page(page)
        for item in response_json['items']:
            name = item.get('name', '')
            description = item.get('description', '')
            unit_price = float(item.get('unit_price', 0))
            formatted_unit_price = "{:.2f}".format(unit_price)
            unit = item.get('unit', '')
            tax_name = item.get('tax_name', '')
            csv_writer.writerow([name, description, formatted_unit_price, unit, tax_name])

print(f"Dados de todos os itens salvos em {output_csv_file}")