import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "zincotech.db")


def conectar():
    return sqlite3.connect(DB_NAME)


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        endereco TEXT,
        observacao TEXT,
        criado_em TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo_cobranca TEXT NOT NULL,
        preco_custo REAL NOT NULL,
        lucro_percentual REAL NOT NULL,
        ativo INTEGER DEFAULT 1,
        criado_em TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chave TEXT UNIQUE NOT NULL,
        valor REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orcamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        cliente_nome TEXT NOT NULL,
        telefone TEXT,
        endereco TEXT,
        status TEXT DEFAULT 'EM ESPERA',
        observacao TEXT,
        valor_total REAL DEFAULT 0,
        criado_em TEXT,
        atualizado_em TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens_orcamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orcamento_id INTEGER NOT NULL,
        tipo_item TEXT NOT NULL,
        descricao TEXT,
        largura REAL,
        espessura REAL,
        comprimento REAL,
        quantidade REAL,
        peso_kg REAL,
        valor_material REAL,
        valor_total REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS acessorios_orcamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orcamento_id INTEGER NOT NULL,
        produto_id INTEGER,
        nome_produto TEXT NOT NULL,
        tipo_cobranca TEXT NOT NULL,
        quantidade REAL NOT NULL,
        preco_unitario REAL NOT NULL,
        lucro_percentual REAL NOT NULL,
        valor_total REAL NOT NULL
    )
    """)

    configs_padrao = [
        ("preco_kg_aluminio", 0),
        ("lucro_aluminio", 0),
        ("mao_de_obra_percentual", 0)
    ]

    for chave, valor in configs_padrao:
        cursor.execute("""
        INSERT OR IGNORE INTO configuracoes (chave, valor)
        VALUES (?, ?)
        """, (chave, valor))

    conn.commit()
    conn.close()


def adicionar_cliente(nome, telefone="", endereco="", observacao=""):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO clientes (nome, telefone, endereco, observacao, criado_em)
    VALUES (?, ?, ?, ?, ?)
    """, (
        nome,
        telefone,
        endereco,
        observacao,
        datetime.now().strftime("%d/%m/%Y %H:%M")
    ))

    conn.commit()
    conn.close()


def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes ORDER BY nome ASC")
    dados = cursor.fetchall()

    conn.close()
    return dados


def buscar_clientes(termo):
    conn = conectar()
    cursor = conn.cursor()

    termo = termo.strip().lower()

    cursor.execute("""
    SELECT *
    FROM clientes
    ORDER BY nome ASC
    """)

    clientes = cursor.fetchall()
    conn.close()

    resultado = []

    for cliente in clientes:
        cliente_id, nome, telefone, endereco, observacao, criado_em = cliente

        texto_busca = (
            f"{nome or ''} "
            f"{telefone or ''} "
            f"{endereco or ''} "
            f"{observacao or ''}"
        ).lower()

        if termo in texto_busca:
            resultado.append(cliente)

    return resultado


def buscar_cliente_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nome, telefone, endereco, observacao, criado_em
    FROM clientes
    WHERE nome = ?
    LIMIT 1
    """, (nome,))

    dado = cursor.fetchone()
    conn.close()
    return dado


def editar_cliente(cliente_id, nome, telefone, endereco, observacao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE clientes
    SET nome = ?, telefone = ?, endereco = ?, observacao = ?
    WHERE id = ?
    """, (nome, telefone, endereco, observacao, cliente_id))

    conn.commit()
    conn.close()


def excluir_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM clientes
    WHERE id = ?
    """, (cliente_id,))

    conn.commit()
    conn.close()


def adicionar_produto(nome, tipo_cobranca, preco_custo, lucro_percentual):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO produtos (nome, tipo_cobranca, preco_custo, lucro_percentual, criado_em)
    VALUES (?, ?, ?, ?, ?)
    """, (
        nome,
        tipo_cobranca,
        float(preco_custo),
        float(lucro_percentual),
        datetime.now().strftime("%d/%m/%Y %H:%M")
    ))

    conn.commit()
    conn.close()


def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nome, tipo_cobranca, preco_custo, lucro_percentual
    FROM produtos
    WHERE ativo = 1
    ORDER BY nome ASC
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados


def buscar_produtos(termo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nome, tipo_cobranca, preco_custo, lucro_percentual
    FROM produtos
    WHERE ativo = 1
      AND (
        nome LIKE ?
        OR tipo_cobranca LIKE ?
      )
    ORDER BY nome ASC
    """, (f"%{termo}%", f"%{termo}%"))

    dados = cursor.fetchall()
    conn.close()
    return dados


def buscar_produto_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        nome,
        tipo_cobranca,
        preco_custo,
        lucro_percentual
    FROM produtos
    WHERE nome = ?
    AND ativo = 1
    LIMIT 1
    """, (nome,))

    resultado = cursor.fetchone()
    conn.close()
    return resultado


def editar_produto(produto_id, nome, tipo_cobranca, preco_custo, lucro_percentual):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE produtos
    SET nome = ?, tipo_cobranca = ?, preco_custo = ?, lucro_percentual = ?
    WHERE id = ?
    """, (
        nome,
        tipo_cobranca,
        float(preco_custo),
        float(lucro_percentual),
        produto_id
    ))

    conn.commit()
    conn.close()


def excluir_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE produtos
    SET ativo = 0
    WHERE id = ?
    """, (produto_id,))

    conn.commit()
    conn.close()


def salvar_configuracao(chave, valor):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO configuracoes (chave, valor)
    VALUES (?, ?)
    """, (chave, float(valor)))

    conn.commit()
    conn.close()


def buscar_configuracao(chave):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,))
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]

    return 0


def salvar_orcamento(cliente_nome, telefone, endereco, observacao, valor_total):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO orcamentos (
        cliente_nome,
        telefone,
        endereco,
        observacao,
        valor_total,
        criado_em,
        atualizado_em
    )
    VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
    """, (
        cliente_nome,
        telefone,
        endereco,
        observacao,
        valor_total
    ))

    orcamento_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return orcamento_id


def salvar_item_orcamento(
        orcamento_id,
        tipo_item,
        descricao,
        largura,
        espessura,
        comprimento,
        quantidade,
        peso_kg,
        valor_material,
        valor_total
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO itens_orcamento (
        orcamento_id,
        tipo_item,
        descricao,
        largura,
        espessura,
        comprimento,
        quantidade,
        peso_kg,
        valor_material,
        valor_total
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        orcamento_id,
        tipo_item,
        descricao,
        largura,
        espessura,
        comprimento,
        quantidade,
        peso_kg,
        valor_material,
        valor_total
    ))

    conn.commit()
    conn.close()


def salvar_acessorio_orcamento(
        orcamento_id,
        produto_id,
        nome_produto,
        tipo_cobranca,
        quantidade,
        preco_unitario,
        lucro_percentual,
        valor_total
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO acessorios_orcamento (
        orcamento_id,
        produto_id,
        nome_produto,
        tipo_cobranca,
        quantidade,
        preco_unitario,
        lucro_percentual,
        valor_total
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        orcamento_id,
        produto_id,
        nome_produto,
        tipo_cobranca,
        quantidade,
        preco_unitario,
        lucro_percentual,
        valor_total
    ))

    conn.commit()
    conn.close()


def listar_orcamentos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        cliente_nome,
        valor_total,
        status,
        criado_em
    FROM orcamentos
    ORDER BY id DESC
    """)

    dados = cursor.fetchall()
    conn.close()

    return dados


def buscar_orcamentos_por_cliente(nome_cliente):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        cliente_nome,
        valor_total,
        status,
        criado_em
    FROM orcamentos
    WHERE cliente_nome LIKE ?
    ORDER BY id DESC
    """, (f"%{nome_cliente}%",))

    dados = cursor.fetchall()
    conn.close()

    return dados


def buscar_orcamento(orcamento_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        cliente_nome,
        telefone,
        endereco,
        status,
        observacao,
        valor_total,
        criado_em
    FROM orcamentos
    WHERE id = ?
    """, (orcamento_id,))

    dado = cursor.fetchone()
    conn.close()
    return dado


def buscar_itens_orcamento(orcamento_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        tipo_item,
        descricao,
        largura,
        espessura,
        comprimento,
        quantidade,
        peso_kg,
        valor_total
    FROM itens_orcamento
    WHERE orcamento_id = ?
    """, (orcamento_id,))

    dados = cursor.fetchall()
    conn.close()

    return dados


def buscar_acessorios_orcamento(orcamento_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        nome_produto,
        tipo_cobranca,
        quantidade,
        preco_unitario,
        lucro_percentual,
        valor_total
    FROM acessorios_orcamento
    WHERE orcamento_id = ?
    ORDER BY nome_produto ASC
    """, (orcamento_id,))

    dados = cursor.fetchall()
    conn.close()
    return dados


def alterar_status_orcamento(orcamento_id, novo_status):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE orcamentos
    SET status = ?,
        atualizado_em = datetime('now')
    WHERE id = ?
    """, (
        novo_status,
        orcamento_id
    ))

    conn.commit()
    conn.close()


def excluir_orcamento(orcamento_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM itens_orcamento
    WHERE orcamento_id = ?
    """, (orcamento_id,))

    cursor.execute("""
    DELETE FROM acessorios_orcamento
    WHERE orcamento_id = ?
    """, (orcamento_id,))

    cursor.execute("""
    DELETE FROM orcamentos
    WHERE id = ?
    """, (orcamento_id,))

    conn.commit()
    conn.close()


def atualizar_orcamento(orcamento_id, valor_total):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE orcamentos
    SET valor_total = ?,
        atualizado_em = datetime('now')
    WHERE id = ?
    """, (valor_total, orcamento_id))

    conn.commit()
    conn.close()


def excluir_itens_orcamento(orcamento_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM itens_orcamento
    WHERE orcamento_id = ?
    """, (orcamento_id,))

    cursor.execute("""
    DELETE FROM acessorios_orcamento
    WHERE orcamento_id = ?
    """, (orcamento_id,))

    conn.commit()
    conn.close()


criar_tabelas()