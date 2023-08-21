import http.client
import csv
import json
import requests

# Autenticação
auth_url = "https://api.zonesoft.org/v2.1/auth/authenticate"
auth_payload = {
    "user": {
        "nif": "seu-nif",
        "nome": "seu-usuario",
        "password": "sua-senha",
        "loja": numero-da-loja
    }
}
auth_headers = {
    "Content-Type": "application/json"
}

auth_response = requests.post(auth_url, json=auth_payload, headers=auth_headers)

if auth_response.status_code == 200:
    auth_data = auth_response.json()
    auth_hash = auth_data.get("Response", {}).get("Content", {}).get("auth_hash")
    if auth_hash:
        print("Autenticação bem-sucedida!")
    else:
        print("Erro na resposta de autenticação.")
        exit()
else:
    print("Erro de autenticação:", auth_response.text)
    exit()


# Dados para importação de produtos
product_url = "https://api.zonesoft.org/v2.1/products/saveInstances"

# Lendo os dados do arquivo CSV com ponto e vírgula como separador
with open("itens.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    next(reader)  # Ignorar o cabeçalho do CSV
    product_instances = []

    for row in reader:
        loja = int(row[0])
        codigo = int(row[1])
        descricao = row[2]
        familia = int(row[3])
        subfamilia = int(row[4])
        unidade = int(row[5])
        iva = float(row[6])
        datacriacao = row[7]  # Use a data correta do CSV
        retalho = int(row[8])
        fundo = row[9]  # Use a cor correta do CSV
        letra = row[10]  # Use a cor correta do CSV
        vendersemstock = int(row[11])
        precovenda = float(row[12])
        codbarras = row[13]
        iva2 = float(row[14])

        product_instance = {
            "loja": loja,
            "codigo": codigo,
            "descricao": descricao,
            "familia": familia,
            "subfam": subfamilia,
            "unidade": unidade,
            "iva": iva,
            "datacriacao": datacriacao,
            "retalho": retalho,
            "fundo": fundo,
            "letra": letra,
            "vendersemstock": vendersemstock,
            "precovenda": precovenda,
            "codbarras": codbarras,
            "iva2": iva2
            # Outros campos do produto...
        }

        product_instances.append(product_instance)
    else:
        print("Linha inválida no arquivo CSV:", row)

    payload = {
        "auth_hash": auth_hash,
        "product": product_instances
    }

    # payload_str = json.dumps(payload)

    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }

    # conn.request("POST", "/v2.1/products/getInstance", payload_str, headers)

    #res = conn.getresponse()
    #data = res.read()

    #print(data.decode("utf-8"))

    response = requests.post(product_url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Produtos importados com sucesso!")
        print("Resposta da API:", response.text)  # Exibir a resposta da API após a importação
    else:
        print("Erro na importação de produtos:", response.text)