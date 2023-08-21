# -*- coding: utf-8 -*-
import http.client
import csv
import json

conn = http.client.HTTPSConnection("empresa.app.invoicexpress.com")

# Lendo os dados do arquivo CSV com ponto e vírgula como separador
with open("itens2.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")  # Especificando o separador como ponto e vírgula
    next(reader)  # Ignorar o cabeçalho do CSV
    for row in reader:
        name = row[0]
        description = row[1]
        unit_price = row[2]

        payload = {
            "item": {
                "name": name,
                "description": description,
                "unit_price": unit_price,
                "unit": "unit",
                "tax": {"name": "IVA23"}
            }
        }

        payload_str = json.dumps(payload)

        headers = {
            'accept': "application/json",
            'content-type': "application/json"
        }

        conn.request("POST", "/items.json?api_key=sua-api-key-aqui", payload_str, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
