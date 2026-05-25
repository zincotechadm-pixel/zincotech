import os
import re
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

from database import (
    buscar_acessorios_orcamento,
    buscar_itens_orcamento,
    buscar_orcamento,
    buscar_cliente_por_nome
)


EMPRESA_NOME = "ZINCOTECH"
ASSINATURA_ARQUIVO = "assinatura.png"


def moeda(valor):
    return f"R$ {float(valor or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def limpar_nome_arquivo(texto):
    texto = re.sub(r"[^A-Za-z0-9_-]+", "_", texto or "")
    return texto.strip("_") or "cliente"


def texto_limitado(texto, limite):
    texto = str(texto or "")

    if "COMBUSTIVEL_OCULTO" in texto.upper():
        texto = texto.replace("COMBUSTIVEL_OCULTO", "")
        texto = texto.replace("COMBUSTÍVEL_OCULTO", "")

    return texto if len(texto) <= limite else texto[:limite - 3] + "..."


def limpar_descricao_pdf(texto):
    texto = str(texto or "")

    partes = texto.split("|")

    partes_limpas = []

    for parte in partes:
        parte_limpa = parte.strip()

        if "COMBUSTIVEL_OCULTO" in parte_limpa.upper():
            continue

        if "COMBUSTÍVEL_OCULTO" in parte_limpa.upper():
            continue

        if parte_limpa:
            partes_limpas.append(parte_limpa)

    return " | ".join(partes_limpas)


def desenhar_linha_tabela(pdf, y, colunas, larguras, header=False):
    x = 2 * cm
    altura_linha = 0.65 * cm

    if header:
        pdf.setFillColorRGB(0, 0, 0)
        pdf.rect(
            x,
            y - altura_linha + 0.1 * cm,
            sum(larguras),
            altura_linha,
            stroke=0,
            fill=1
        )
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 8)
    else:
        pdf.setFillColorRGB(0.1, 0.1, 0.1)
        pdf.setFont("Helvetica", 8)

    atual_x = x

    for texto, largura_coluna in zip(colunas, larguras):
        pdf.drawString(
            atual_x + 0.12 * cm,
            y - 0.35 * cm,
            texto_limitado(texto, int(largura_coluna / 8))
        )
        atual_x += largura_coluna

    if not header:
        pdf.setStrokeColorRGB(0.75, 0.75, 0.75)
        pdf.line(
            x,
            y - altura_linha + 0.05 * cm,
            x + sum(larguras),
            y - altura_linha + 0.05 * cm
        )

    return y - altura_linha


def gerar_pdf_orcamento(
    orcamento_id,
    cliente,
    valor_total,
    status,
    data,
    nome_arquivo=None
):
    cliente_arquivo = limpar_nome_arquivo(cliente)

    pasta_app = os.path.dirname(os.path.abspath(__file__))

    pasta_saida = os.path.join(
        pasta_app,
        "arquivos_gerados",
        "pdf_orcamentos"
    )

    os.makedirs(pasta_saida, exist_ok=True)

    nome_arquivo = (
        nome_arquivo
        or os.path.join(
            pasta_saida,
            f"orcamento_{orcamento_id}_{cliente_arquivo}.pdf"
        )
    )

    dados_orcamento = buscar_orcamento(orcamento_id)

    telefone = dados_orcamento[2] if dados_orcamento else ""
    endereco = dados_orcamento[3] if dados_orcamento else ""

    if not telefone or not endereco:
        cliente_dados = buscar_cliente_por_nome(cliente)

        if cliente_dados:
            if not telefone:
                telefone = cliente_dados[2] or ""

            if not endereco:
                endereco = cliente_dados[3] or ""

    pdf = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    modelo = os.path.join(pasta_app, "modelo_orcamento.png")
    assinatura_path = os.path.join(pasta_app, ASSINATURA_ARQUIVO)

    if os.path.exists(modelo):
        pdf.drawImage(modelo, 0, 0, width=largura, height=altura)
    else:
        pdf.setFillColorRGB(1, 1, 1)
        pdf.rect(0, 0, largura, altura, stroke=0, fill=1)

    data_atual = datetime.now().strftime("%d/%m/%Y")

    pdf.setFillColorRGB(1, 1, 1)
    pdf.rect(
        11.8 * cm,
        altura - 6.1 * cm,
        7.5 * cm,
        1.1 * cm,
        stroke=0,
        fill=1
    )

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(
        18.9 * cm,
        altura - 5.35 * cm,
        f"Guaramirim, {data_atual}."
    )

    y = altura - 8.1 * cm

    pdf.setFillColorRGB(0.1, 0.1, 0.1)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(2 * cm, y, f"CLIENTE: {cliente}")

    y -= 0.45 * cm
    pdf.setFont("Helvetica", 9)
    pdf.drawString(2 * cm, y, f"WHATSAPP: {telefone or '-'}")

    y -= 0.45 * cm
    pdf.drawString(2 * cm, y, f"ENDEREÇO: {endereco or '-'}")

    y -= 0.8 * cm

    numero_visual = 1047 + int(orcamento_id)

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(2 * cm, y, f"ORÇAMENTO: {numero_visual}")

    y -= 0.45 * cm
    pdf.setFont("Helvetica", 9)
    pdf.drawString(2 * cm, y, f"STATUS: {status}")

    y -= 0.45 * cm
    pdf.drawString(2 * cm, y, f"DATA: {data}")

    y -= 1 * cm

    itens = buscar_itens_orcamento(orcamento_id)

    larguras = [
        3.2 * cm,
        5.0 * cm,
        2.3 * cm,
        2.0 * cm,
        2.5 * cm,
        2.3 * cm
    ]

    y = desenhar_linha_tabela(
        pdf,
        y,
        ["TIPO", "DESCRIÇÃO", "CORTE", "COMP.", "QTD", "KG"],
        larguras,
        header=True
    )

    total_kg = 0

    for item in itens:
        (
            item_id,
            tipo,
            descricao,
            largura_i,
            espessura,
            comprimento,
            quantidade,
            peso_kg,
            valor_item
        ) = item

        descricao_pdf = limpar_descricao_pdf(descricao)

        if not descricao_pdf:
            descricao_pdf = "-"

        try:
            kg_item = float(peso_kg or 0)
        except:
            kg_item = 0

        total_kg += kg_item

        y = desenhar_linha_tabela(
            pdf,
            y,
            [
                str(tipo),
                str(descricao_pdf),
                f"{largura_i:g} cm",
                f"{comprimento:g} m",
                f"{quantidade:g}",
                f"{kg_item:.2f}kg"
            ],
            larguras
        )

    acessorios = buscar_acessorios_orcamento(orcamento_id)

    if acessorios:
        y -= 0.8 * cm

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(2 * cm, y, "MATERIAIS INCLUSOS")

        y -= 0.45 * cm

        larg_ac = [9 * cm, 3 * cm, 3 * cm]

        y = desenhar_linha_tabela(
            pdf,
            y,
            ["PRODUTO", "QTD", "UNIDADE"],
            larg_ac,
            header=True
        )

        for acessorio in acessorios:
            (
                acessorio_id,
                nome,
                tipo,
                quantidade,
                preco_unitario,
                lucro,
                valor_item
            ) = acessorio

            nome_limpo = str(nome or "")

            if "COMBUSTIVEL" in nome_limpo.upper():
                continue

            if "COMBUSTÍVEL" in nome_limpo.upper():
                continue

            y = desenhar_linha_tabela(
                pdf,
                y,
                [
                    str(nome),
                    f"{quantidade:g}",
                    str(tipo)
                ],
                larg_ac
            )

    y -= 0.8 * cm

    pdf.setFont("Helvetica-Bold", 11)
    pdf.setFillColorRGB(0.1, 0.1, 0.1)
    pdf.drawRightString(
        largura - 2 * cm,
        y,
        f"TOTAL KG: {total_kg:.2f}kg"
    )

    y -= 0.6 * cm

    pdf.setFillColorRGB(0.70, 0, 0)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawRightString(
        largura - 2 * cm,
        y,
        f"VALOR DO ORÇAMENTO: {moeda(valor_total)}"
    )

    y -= 1.0 * cm

    pdf.setFillColorRGB(0.1, 0.1, 0.1)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(2 * cm, y, "PRAZO DE ENTREGA:")

    y -= 0.45 * cm

    pdf.setFont("Helvetica", 9)
    pdf.drawString(2 * cm, y, "A combinar com o cliente.")

    y -= 1.6 * cm

    if os.path.exists(assinatura_path):
        try:
            pdf.drawImage(
                assinatura_path,
                2.3 * cm,
                y - 0.1 * cm,
                width=5 * cm,
                height=1.3 * cm,
                preserveAspectRatio=True,
                mask="auto"
            )
        except Exception:
            pass

    pdf.setStrokeColorRGB(0.25, 0.25, 0.25)

    pdf.line(2 * cm, y - 0.35 * cm, 8.5 * cm, y - 0.35 * cm)
    pdf.line(11 * cm, y - 0.35 * cm, 18.8 * cm, y - 0.35 * cm)

    pdf.setFillColorRGB(0.1, 0.1, 0.1)
    pdf.setFont("Helvetica", 9)

    pdf.drawCentredString(5.25 * cm, y - 0.85 * cm, "Assinatura Responsável")
    pdf.drawCentredString(14.9 * cm, y - 0.85 * cm, "Aceite do Cliente")

    pdf.save()

    return nome_arquivo