from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

from database import (
    listar_clientes,
    salvar_orcamento,
    salvar_item_orcamento,
    buscar_produto_por_nome,
    buscar_orcamento,
    buscar_itens_orcamento,
    atualizar_orcamento,
    excluir_itens_orcamento
)

from calculos import calcular_item, aplicar_mao_de_obra


class TelaOrcamentos(Screen):

    def carregar_clientes_spinner(self):
        clientes = listar_clientes()
        nomes_clientes = [cliente[1] for cliente in clientes] or ["SEM CLIENTES"]

        self.cliente.values = nomes_clientes
        self.cliente.text = "SELECIONE O CLIENTE"

    def on_pre_enter(self):
        self.carregar_clientes_spinner()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.itens = []
        self.orcamento_editando_id = None
        self.item_editando_indice = None

        principal = BoxLayout(
            orientation="vertical",
            padding=4,
            spacing=2
        )

        self.titulo = Label(
            text="NOVO ORÇAMENTO",
            font_size="15sp",
            bold=True,
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=26
        )
        principal.add_widget(self.titulo)

        clientes = listar_clientes()
        nomes_clientes = [cliente[1] for cliente in clientes] or ["SEM CLIENTES"]

        self.cliente = Spinner(
            text="SELECIONE O CLIENTE",
            values=nomes_clientes,
            size_hint_y=None,
            height=30
        )
        principal.add_widget(self.cliente)

        self.tipo_item = Spinner(
            text="CALHA",
            values=("CALHA", "RUFO", "COLARINHO", "PINGADEIRA"),
            size_hint_y=None,
            height=30
        )
        principal.add_widget(self.tipo_item)

        self.descricao = self.campo("Descrição")
        principal.add_widget(self.descricao)

        linha1 = BoxLayout(spacing=3, size_hint_y=None, height=30)

        self.largura = self.campo("Largura CM")
        self.espessura = self.campo("Espessura")
        self.largura.input_filter = "float"
        self.espessura.input_filter = "float"

        linha1.add_widget(self.largura)
        linha1.add_widget(self.espessura)
        principal.add_widget(linha1)

        linha2 = BoxLayout(spacing=3, size_hint_y=None, height=30)

        self.comprimento = self.campo("Comprimento M")
        self.quantidade = self.campo("Quantidade")
        self.comprimento.input_filter = "float"
        self.quantidade.input_filter = "float"

        linha2.add_widget(self.comprimento)
        linha2.add_widget(self.quantidade)
        principal.add_widget(linha2)

        linha_saida = BoxLayout(spacing=3, size_hint_y=None, height=30)

        self.saida_tipo = Spinner(
            text="SAÍDA",
            values=("75MM", "100MM", "150MM"),
            size_hint_x=0.5
        )
        self.saida_quantidade = self.campo("Qtd Saídas")
        self.saida_quantidade.input_filter = "float"

        linha_saida.add_widget(self.saida_tipo)
        linha_saida.add_widget(self.saida_quantidade)
        principal.add_widget(linha_saida)

        linha_tubo = BoxLayout(spacing=3, size_hint_y=None, height=30)

        self.tubo_tipo = Spinner(
            text="TUBO",
            values=("75MM", "100MM"),
            size_hint_x=0.5
        )
        self.tubo_quantidade = self.campo("Qtd Tubos")
        self.tubo_quantidade.input_filter = "float"

        linha_tubo.add_widget(self.tubo_tipo)
        linha_tubo.add_widget(self.tubo_quantidade)
        principal.add_widget(linha_tubo)

        linha_suporte = BoxLayout(spacing=3, size_hint_y=None, height=30)

        self.suporte_tipo = Spinner(
            text="SUPORTE",
            values=("25CM", "30CM", "40CM", "50CM", "60CM", "70CM", "80CM", "90CM", "100CM"),
            size_hint_x=0.5
        )
        self.suporte_quantidade = self.campo("Qtd Suportes")
        self.suporte_quantidade.input_filter = "float"

        linha_suporte.add_widget(self.suporte_tipo)
        linha_suporte.add_widget(self.suporte_quantidade)
        principal.add_widget(linha_suporte)

        linha_curva = BoxLayout(spacing=3, size_hint_y=None, height=30)

        self.curva_tipo = Spinner(
            text="CURVA",
            values=("75MM", "100MM"),
            size_hint_x=0.5
        )
        self.curva_quantidade = self.campo("Qtd Curvas")
        self.curva_quantidade.input_filter = "float"

        linha_curva.add_widget(self.curva_tipo)
        linha_curva.add_widget(self.curva_quantidade)
        principal.add_widget(linha_curva)

        linha_pu = BoxLayout(spacing=3, size_hint_y=None, height=30)

        self.pu_tipo = Spinner(
            text="PU",
            values=("PU",),
            size_hint_x=0.5
        )
        self.pu_quantidade = self.campo("Qtd PU")
        self.pu_quantidade.input_filter = "float"

        linha_pu.add_widget(self.pu_tipo)
        linha_pu.add_widget(self.pu_quantidade)
        principal.add_widget(linha_pu)

        linha_corrente = BoxLayout(spacing=3, size_hint_y=None, height=30)

        self.corrente_tipo = Spinner(
            text="CORRENTE",
            values=("CORRENTE",),
            size_hint_x=0.5
        )
        self.corrente_metros = self.campo("Metros Corrente")
        self.corrente_metros.input_filter = "float"

        linha_corrente.add_widget(self.corrente_tipo)
        linha_corrente.add_widget(self.corrente_metros)
        principal.add_widget(linha_corrente)

        linha_combustivel = BoxLayout(spacing=3, size_hint_y=None, height=30)

        self.combustivel_tipo = Spinner(
            text="COMBUSTÍVEL",
            values=("COMBUSTÍVEL",),
            size_hint_x=0.5
        )
        self.combustivel_valor = self.campo("Valor Combustível")
        self.combustivel_valor.input_filter = "float"

        linha_combustivel.add_widget(self.combustivel_tipo)
        linha_combustivel.add_widget(self.combustivel_valor)
        principal.add_widget(linha_combustivel)

        self.btn_add = Button(
            text="ADICIONAR ITEM",
            background_color=(0.75, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=None,
            height=34,
            font_size="12sp"
        )
        self.btn_add.bind(on_press=self.adicionar_ou_atualizar_item)
        principal.add_widget(self.btn_add)

        principal.add_widget(Label(
            text="ITENS DO ORÇAMENTO",
            font_size="13sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=22
        ))

        scroll = ScrollView()

        self.lista_itens = BoxLayout(
            orientation="vertical",
            spacing=2,
            size_hint_y=None
        )
        self.lista_itens.bind(minimum_height=self.lista_itens.setter("height"))

        scroll.add_widget(self.lista_itens)
        principal.add_widget(scroll)

        self.total_label = Label(
            text="TOTAL: R$ 0.00",
            font_size="15sp",
            bold=True,
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=30
        )
        principal.add_widget(self.total_label)

        linha_botoes = BoxLayout(spacing=3, size_hint_y=None, height=34)

        self.btn_salvar = Button(
            text="SALVAR",
            background_color=(0.75, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size="12sp"
        )
        self.btn_salvar.bind(on_press=self.salvar)

        btn_limpar = Button(
            text="LIMPAR",
            background_color=(0.25, 0.25, 0.25, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size="12sp"
        )
        btn_limpar.bind(on_press=self.limpar_tela)

        linha_botoes.add_widget(self.btn_salvar)
        linha_botoes.add_widget(btn_limpar)
        principal.add_widget(linha_botoes)

        btn_voltar = Button(
            text="VOLTAR",
            background_color=(0.12, 0.12, 0.12, 1),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=None,
            height=34,
            font_size="12sp"
        )
        btn_voltar.bind(on_press=self.voltar)
        principal.add_widget(btn_voltar)

        self.add_widget(principal)
        self.atualizar_lista_itens()

    def campo(self, dica):
        return TextInput(
            hint_text=dica,
            multiline=False,
            size_hint_y=None,
            height=30,
            font_size="12sp",
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(1, 0, 0, 1),
            padding=[5, 5, 5, 5]
        )

    def calcular_produto_extra(self, nome_produto, quantidade):
        produto = buscar_produto_por_nome(nome_produto)

        if not produto:
            print(f"Produto não encontrado: {nome_produto}")
            return 0

        produto_id, nome, tipo, preco, lucro = produto
        preco_final = float(preco) + (float(preco) * float(lucro) / 100)

        return preco_final * float(quantidade or 0)

    def adicionar_ou_atualizar_item(self, instance):
        try:
            largura = float(self.largura.text)
            espessura = float(self.espessura.text)
            comprimento = float(self.comprimento.text)
            quantidade = float(self.quantidade.text)
        except:
            print("Preencha corretamente")
            return

        calculo = calcular_item(largura, comprimento, espessura)
        valor_total = calculo["valor"] * quantidade

        extras = []

        qtd = float(self.saida_quantidade.text or 0)
        if qtd > 0:
            nome = f"SAIDA {self.saida_tipo.text}"
            valor_total += self.calcular_produto_extra(nome, qtd)
            extras.append(f"Saída {self.saida_tipo.text}: {qtd:g}")

        qtd = float(self.tubo_quantidade.text or 0)
        if qtd > 0:
            nome = f"TUBO ALUMINIO {self.tubo_tipo.text}"
            valor_total += self.calcular_produto_extra(nome, qtd)
            extras.append(f"Tubo {self.tubo_tipo.text}: {qtd:g}")

        qtd = float(self.suporte_quantidade.text or 0)
        if qtd > 0:
            nome = f"SUPORTE {self.suporte_tipo.text}"
            valor_total += self.calcular_produto_extra(nome, qtd)
            extras.append(f"Suporte {self.suporte_tipo.text}: {qtd:g}")

        qtd = float(self.curva_quantidade.text or 0)
        if qtd > 0:
            nome = f"CURVA {self.curva_tipo.text}"
            valor_total += self.calcular_produto_extra(nome, qtd)
            extras.append(f"Curva {self.curva_tipo.text}: {qtd:g}")

        qtd = float(self.pu_quantidade.text or 0)
        if qtd > 0:
            valor_total += self.calcular_produto_extra("PU", qtd)
            extras.append(f"PU: {qtd:g}")

        qtd = float(self.corrente_metros.text or 0)
        if qtd > 0:
            valor_total += self.calcular_produto_extra("CORRENTE", qtd)
            extras.append(f"Corrente: {qtd:g}m")

        combustivel = float(self.combustivel_valor.text or 0)
        if combustivel > 0:
            valor_total += combustivel
            extras.append("COMBUSTIVEL_OCULTO")

        descricao_final = self.descricao.text

        extras_visiveis = [
            extra for extra in extras
            if extra != "COMBUSTIVEL_OCULTO"
        ]

        if extras_visiveis:
            descricao_final += " | " + " | ".join(extras_visiveis)

        item = {
            "tipo": self.tipo_item.text,
            "descricao": descricao_final,
            "largura": largura,
            "espessura": espessura,
            "comprimento": comprimento,
            "quantidade": quantidade,
            "peso_kg": calculo["peso_kg"],
            "valor": valor_total
        }

        self.itens.append(item)

        print("Item adicionado")

        self.limpar_campos_item()
        self.atualizar_lista_itens()

    def limpar_campos_item(self):
        self.descricao.text = ""
        self.largura.text = ""
        self.espessura.text = ""
        self.comprimento.text = ""
        self.quantidade.text = ""

        self.saida_quantidade.text = ""
        self.tubo_quantidade.text = ""
        self.suporte_quantidade.text = ""
        self.curva_quantidade.text = ""
        self.pu_quantidade.text = ""
        self.corrente_metros.text = ""
        self.combustivel_valor.text = ""

    def atualizar_lista_itens(self):
        self.lista_itens.clear_widgets()

        total = 0

        if not self.itens:
            self.lista_itens.add_widget(Label(
                text="Nenhum item adicionado ainda.",
                color=(0.8, 0.8, 0.8, 1),
                size_hint_y=None,
                height=30,
                font_size="12sp"
            ))

        for item in self.itens:
            total += item["valor"]

            texto = (
                f'{item["tipo"]} - {item["descricao"]}\n'
                f'R$ {item["valor"]:.2f}'
            )

            self.lista_itens.add_widget(Label(
                text=texto,
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=40,
                font_size="12sp"
            ))

        total_com_mao_de_obra = aplicar_mao_de_obra(total)
        self.total_label.text = f"TOTAL: R$ {total_com_mao_de_obra:.2f}"

    def salvar(self, instance):
        if not self.itens:
            print("Nenhum item")
            return

        cliente = self.cliente.text

        if cliente == "SELECIONE O CLIENTE" or cliente == "SEM CLIENTES":
            print("Selecione um cliente")
            return

        subtotal = sum(item["valor"] for item in self.itens)
        total = aplicar_mao_de_obra(subtotal)

        if self.orcamento_editando_id:
            excluir_itens_orcamento(self.orcamento_editando_id)
            atualizar_orcamento(self.orcamento_editando_id, total)
            orcamento_id = self.orcamento_editando_id
        else:
            orcamento_id = salvar_orcamento(
                cliente,
                "",
                "",
                "",
                total
            )

        for item in self.itens:
            salvar_item_orcamento(
                orcamento_id,
                item["tipo"],
                item["descricao"],
                item["largura"],
                item["espessura"],
                item["comprimento"],
                item["quantidade"],
                item["peso_kg"],
                item["valor"],
                item["valor"]
            )

        print("ORÇAMENTO SALVO")

        self.limpar_tela()

    def carregar_para_edicao(self, orcamento_id, *args):
        dados = buscar_orcamento(orcamento_id)

        if not dados:
            print("Orçamento não encontrado")
            return

        self.orcamento_editando_id = orcamento_id

        cliente = dados[1]

        self.carregar_clientes_spinner()
        self.cliente.text = cliente

        self.itens.clear()

        itens = buscar_itens_orcamento(orcamento_id)

        for item in itens:
            (
                item_id,
                tipo,
                descricao,
                largura,
                espessura,
                comprimento,
                quantidade,
                peso_kg,
                valor_total
            ) = item

            self.itens.append({
                "tipo": tipo,
                "descricao": descricao,
                "largura": largura,
                "espessura": espessura,
                "comprimento": comprimento,
                "quantidade": quantidade,
                "peso_kg": peso_kg,
                "valor": valor_total
            })

        self.titulo.text = "EDITAR ORÇAMENTO"
        self.btn_salvar.text = "ATUALIZAR"
        self.atualizar_lista_itens()
        self.manager.current = "orcamentos"

    def limpar_tela(self, instance=None):
        self.itens.clear()
        self.lista_itens.clear_widgets()
        self.total_label.text = "TOTAL: R$ 0.00"
        self.orcamento_editando_id = None
        self.item_editando_indice = None
        self.titulo.text = "NOVO ORÇAMENTO"
        self.btn_salvar.text = "SALVAR"
        self.cliente.text = "SELECIONE O CLIENTE"
        self.limpar_campos_item()
        self.atualizar_lista_itens()

    def voltar(self, instance):
        self.manager.current = "inicio"