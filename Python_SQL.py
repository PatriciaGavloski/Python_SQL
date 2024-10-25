"""
Projeto

Se conectar com o banco de dados da oracle para fazer uma pesquisa, consultado as informações da base de dados.
Existe um modelo pre estabelecido de como esses dados serão armazenados 
Os dados serão armazenados em um arquivo xml com todas as linhas da consulta. 
XML tem um padrão especifico
Cada Coluna da pesquisa deve ser armazenada dentro da tag no modelo pre estabelecido.
No final será gerado apenas um arquivo xml com todas as informações pesquisadas no banco de dados
Organizados conforme o Modelo.

Desenvolvendo o código 

1. Planejamento 

* Conexão com banco de dados Oracle 
* Executar uma consulta SQL → Query 
* Espicificar cada coluna do banco de dados para uma tag no modelo xml 
* Gerar o arquivo XML

2. Instalação das Configurações Necessárias 

Para poder conectar com a senha do Oracle é preciso ser instalado um pacote o ORACLE INSTANT CLIENT
Esse pacote deve ser baixado o driver instantclient-basic-windows.x64-23.5.0.24.07
Ou Superior 

Depois do Download é realizado a extração dos arquivos que deveram estar no dispositivo C do 
Computador 

será necessario copiar o caminho da pasta 

Clicando com o lado direito do mouse na logo do windows em iniciar 
Selecione = sistemas 
Selecione = Configurações avançadas do sistema
Na Aba Avançado 
Selecione = Variável de Ambiente 
Selecione = Path e edite 
Cole o endereço do diretório do instantclient-basic-windows.x64-23.5.0.24.07

Instalar
Depois dentro do Visual Studio Code no terminal 
pip install oracledb
 
"""

#BIBLIOTECAS USADAS 
#Biblioteca OS faz conexão do código com o sistema operacional 
#Biblioteca Oracledb faz conexão do código com o Banco de dados 

import os
import oracledb

#Indicar onde está o pacote da Oracle no PC

oracledb.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-23.5.0.24.07\instantclient_23_5")

#Função para conectar ao banco de dados 


def conectar_banco():
    try:
        dsn = oracledb.makedsn('SERVER HOST', PORTA, service_name='NOME')
        conexao = oracledb.connect(user='USUARIO', password='SENHA', dsn=dsn)
        print("Conexão com o banco de dados bem-sucedida!")
        return conexao
    except oracledb.DatabaseError as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

def buscar_query(conexao):
    try:
        cursor = conexao.cursor()

        query = """
SELECT DISTINCT 
    CASE VF.tipo_familia
        WHEN 'A' THEN 'AUTOMOVEL'
        WHEN 'M' THEN 'MOTO'
        WHEN 'C' THEN 'CAMINHÃO'
        ELSE 'TIPO NÃO DEFINIDO'
    END AS tipo_familia, VV.CHASSI,
    VM.DES_MODELO,
    VM.marca_veiculo, 
    VM.MODELO,
    OFS.ano_modelo,
    OFS.ANO_FABRICACAO,
    CASE VV.NOVO_USADO
        WHEN 'U' THEN 'SEMI-NOVO'
        ELSE VV.NOVO_USADO
    END AS NOVO_USADO,
    OFS.km_atual, 
    CASE OFS.COMBUSTIVEL 
        WHEN 'G' THEN 'GASOLINA' 
        WHEN 'B' THEN 'FLEX' 
        WHEN 'A' THEN 'ALCOOL'
        WHEN 'D' THEN 'DIESEL' 
        WHEN 'S' THEN 'GAS' 
        WHEN 'T' THEN 'TRI-COMBUSTIVEL' 
        ELSE 'NAO DEFINIDO' 
    END AS COMBUSTIVEL,
    OFS.motor,
    OFS.placa,
    OFS.portas,
    VV.cor, 
    VV.preco_concessionaria AS preco_veiculo,
    VV.preco_minimo_comercializacao
FROM 
    vei_veiculo VV
LEFT OUTER JOIN
    VEI_MODELO VM ON VM.EMPRESA = VV.EMPRESA AND VM.MODELO = VV.MODELO
LEFT OUTER JOIN
    OFI_FICHA_SEGUIMENTO OFS ON OFS.CHASSI = VV.CHASSI
LEFT OUTER JOIN
    VEI_FAMILIA VF ON VF.FAMILIA = VM.FAMILIA AND VF.EMPRESA = VV.EMPRESA
JOIN 
    GER_REVENDA GR ON GR.EMPRESA = VV.EMPRESA AND GR.REVENDA = VV.revenda_origem
WHERE 
    VV.situacao = 'ES' 
    AND VV.NOVO_USADO = 'U'ORDER BY ofs.placa 
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()

        if resultados:
            gerar_xml(resultados)

    except oracledb.DatabaseError as err:
        print(f"Erro ao executar a query: {err}")
    
    finally:
        cursor.close()
        conexao.close()

#Função para gerar o XML com base no resultado

"""
Cada numero em \n{row[24]}\n  é o numero da coluna que está a informação da linha 
Nesse explemplo a coluna 24 contem a informação da Descrição do Veículo 
"""

def gerar_xml(resultados):
    xml_content = ""

    for row in resultados:
        valores = {
"ID": "Em Branco",  
            "DATE": "Em Branco",  
            "TITLE": "Em Branco",  
            "CATEGORY": str(row[0]), 
            "DESCRIPTION": str(row[2]), 
            "ACCESSORIES": "Em Branco",  
            "MAKE": str(row[3]), 
            "MODEL": str(row[4]),
            "YEAR": str(row[5]),  
            "FABRIC_YEAR": str(row[6]), 
            "CONDITION": str(row[7]),  
            "MILEAGE": str(row[8]) + 'KM', 
            "FUEL": str(row[9]), 
            "GEAR": "Em Branco",  
            "MOTOR": str(row[10]),  
            "PLATE": str(row[11]), 
            "CHASSI": "Em Branco",   
            "DOORS": str(row[12]), 
            "COLOR": str(row[13]),  
            "PRICE": 'R$' + str(row[14]),  
            "SELLER": "Em Branco", 
            "PHONE": "Em Branco",  
            "CNPJ": "Em Branco", 
            "LOCATION_COUNTRY": "BR",  
            "LOCATION_STATE": "Em Branco", 
            "LOCATION_CITY": "Em Branco",
            "ZIP_CODE": "Em Branco", 
            "NEIGHBORHOOD": "Em Branco", 
            "STREET": "Em Branco",
            "NUMBER": "Em Branco", 
            "IMAGES": "Em Branco",  
            "FIPE": "Em Branco",  
            "VALOR_FIPE": "Em Branco",  
            "LAST_UPDATE": "Em Branco",
            "PROMOTION_PRICE": str(row[15]),    
            "BODY_TYPE": "Em Branco",  
            "HP": "Em Branco",  
            "BASE_MODEL": "Em Branco",  
            "IMAGES_LARGE": "Em Branco",   
        }

        xml_content += "<AD>\n\n"
        for tag, valor in valores.items():
            xml_content += f"  <!-- {tag} -->\n"
            xml_content += f"  <{tag}>{valor if valor != 'Em Branco' else ''}</{tag}>\n\n"
        xml_content += "</AD>\n\n"  

    nome_arquivo = "veiculos.xml"
    caminho = os.path.join(os.getcwd(), nome_arquivo)

    with open(caminho, 'w', encoding='utf-8') as file:
        file.write(xml_content)

    print(f"Arquivo XML gerado com sucesso: {caminho}")


conexao = conectar_banco()
if conexao:
    buscar_query(conexao)
