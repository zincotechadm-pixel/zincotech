import math

from database import buscar_configuracao, listar_produtos


def buscar_aluminio_kg():
    preco_config = buscar_configuracao("preco_kg_aluminio")
    lucro_config = buscar_configuracao("lucro_aluminio")

    return float(preco_config), float(lucro_config)


def normalizar_texto(texto):
    return (texto or "").strip().upper()


def buscar_produto_por_nome(*nomes):
    produtos = listar_produtos()
    nomes_normalizados = [normalizar_texto(nome) for nome in nomes]

    for produto in produtos:
        produto_id, nome, tipo, preco, lucro = produto
        nome_normalizado = normalizar_texto(nome)

        if any(nome_busca in nome_normalizado for nome_busca in nomes_normalizados):
            return {
                "id": produto_id,
                "nome": nome,
                "tipo": tipo,
                "preco": float(preco),
                "lucro": float(lucro)
            }

    return None


def calcular_area_m2(largura_cm, comprimento_m, quantidade=1):
    largura_m = float(largura_cm) / 100
    area = largura_m * float(comprimento_m) * float(quantidade)

    return round(area, 3)


def calcular_peso_kg(largura_cm, comprimento_m, espessura_mm):
    area_m2 = calcular_area_m2(largura_cm, comprimento_m)
    peso = area_m2 * float(espessura_mm) * 2.70

    return round(peso, 2)


def calcular_valor_aluminio(peso_kg):
    preco_kg, lucro = buscar_aluminio_kg()

    valor_base = peso_kg * preco_kg

    valor_final = valor_base + (valor_base * lucro / 100)

    return round(valor_final, 2)


def calcular_item(largura_cm, comprimento_m, espessura_mm):
    area = calcular_area_m2(
        largura_cm,
        comprimento_m
    )

    peso = calcular_peso_kg(
        largura_cm,
        comprimento_m,
        espessura_mm
    )

    valor = calcular_valor_aluminio(peso)

    return {
        "area_m2": area,
        "peso_kg": peso,
        "valor": valor
    }


def calcular_acessorio(quantidade, preco_unitario, lucro_percentual):
    valor = quantidade * preco_unitario
    valor += valor * (lucro_percentual / 100)

    return round(valor, 2)


def montar_acessorio_calculado(produto, nome_padrao, quantidade):
    quantidade = float(quantidade)

    if produto:
        nome = produto["nome"]
        produto_id = produto["id"]
        tipo = produto["tipo"]
        preco = produto["preco"]
        lucro = produto["lucro"]
    else:
        nome = nome_padrao
        produto_id = None
        tipo = "UNIDADE"
        preco = 0
        lucro = 0

    return {
        "produto_id": produto_id,
        "nome": nome,
        "tipo": tipo,
        "quantidade": quantidade,
        "preco_unitario": preco,
        "lucro_percentual": lucro,
        "valor_total": calcular_acessorio(quantidade, preco, lucro)
    }


def calcular_acessorios_automaticos(largura_cm, comprimento_m, quantidade):
    quantidade = float(quantidade)
    total_metros = float(comprimento_m) * quantidade
    total_pontas = 2 * quantidade

    rebites_por_ponta = math.ceil(float(largura_cm) / 3)
    rebites = rebites_por_ponta * total_pontas

    parafusos = math.ceil(float(comprimento_m) / 0.60) * quantidade
    buchas = parafusos

    tubos_pu_comprimento = math.ceil(total_metros / 5) if total_metros > 0 else 0
    tubos_pu_pontas = math.ceil(total_pontas / 2) if total_pontas > 0 else 0
    tubos_pu = tubos_pu_comprimento + tubos_pu_pontas

    return [
        montar_acessorio_calculado(
            buscar_produto_por_nome("REBITE"),
            "Rebite",
            rebites
        ),
        montar_acessorio_calculado(
            buscar_produto_por_nome("PARAFUSO"),
            "Parafuso",
            parafusos
        ),
        montar_acessorio_calculado(
            buscar_produto_por_nome("BUCHA"),
            "Bucha",
            buchas
        ),
        montar_acessorio_calculado(
            buscar_produto_por_nome("PU", "VEDA", "SELANTE"),
            "Tubo de PU",
            tubos_pu
        )
    ]


def aplicar_mao_de_obra(valor_total):
    mao_de_obra = buscar_configuracao("mao_de_obra_percentual")

    total = valor_total + (valor_total * mao_de_obra / 100)

    return round(total, 2)


def calcular_total_geral(itens, acessorios):
    total = 0

    for item in itens:
        total += item["valor"]

    for acessorio in acessorios:
        total += acessorio["valor_total"]

    total = aplicar_mao_de_obra(total)

    return round(total, 2)
