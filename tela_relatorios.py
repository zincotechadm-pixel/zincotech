from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from database import (
    listar_orcamentos,
    buscar_orcamentos_por_cliente,
    buscar_orcamento,
    buscar_itens_orcamento,
    alterar_status_orcamento
)


class TelaRelatorios(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        principal = BoxLayout(orientation="vertical", padding=10, spacing=8)

        self.titulo = Label(
            text="RELATÓRIOS",
            font_size="22sp",
            bold=True,
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=42
        )
        principal.add_widget(self.titulo)

        self.resumo = Label(
            text="",
            font_size="13sp",
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=95
        )
        principal.add_widget(self.resumo)

        self.busca = TextInput(
            hint_text="Buscar cliente",
            multiline=False,
            size_hint_y=None,
            height=42,
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(1, 0, 0, 1),
            padding=[10, 10, 10, 10]
        )
        principal.add_widget(self.busca)

        linha_busca = BoxLayout(spacing=5, size_hint_y=None, height=42)

        btn_buscar = Button(text="BUSCAR", background_color=(0.75, 0, 0, 1), color=(1, 1, 1, 1), bold=True)
        btn_buscar.bind(on_press=self.buscar_cliente)

        btn_todos = Button(text="TODOS", background_color=(0.20, 0.20, 0.20, 1), color=(1, 1, 1, 1), bold=True)
        btn_todos.bind(on_press=self.carregar_todos)

        linha_busca.add_widget(btn_buscar)
        linha_busca.add_widget(btn_todos)
        principal.add_widget(linha_busca)

        scroll = ScrollView()

        self.lista = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter("height"))

        scroll.add_widget(self.lista)
        principal.add_widget(scroll)

        btn_voltar = Button(
            text="VOLTAR",
            background_color=(0.12, 0.12, 0.12, 1),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=None,
            height=52
        )
        btn_voltar.bind(on_press=self.voltar)
        principal.add_widget(btn_voltar)

        self.add_widget(principal)

    def on_pre_enter(self, *args):
        self.carregar_todos()

    def moeda(self, valor):
        return f"R$ {float(valor or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def carregar_todos(self, instance=None):
        try:
            self.busca.text = ""
            orcamentos = listar_orcamentos()
            self.atualizar_resumo(orcamentos)
            self.mostrar_orcamentos(orcamentos, "TODOS")
        except Exception as erro:
            self.mostrar_mensagem(f"Erro ao abrir relatório:\n{erro}")

    def atualizar_resumo(self, orcamentos):
        espera = aprovado = andamento = concluido = negado = 0

        for orc in orcamentos:
            orc_id, cliente, valor, status, data = orc
            s = str(status).upper()

            if "ESPERA" in s:
                espera += 1
            elif "APROV" in s:
                aprovado += 1
            elif "ANDAMENTO" in s or "EXECU" in s:
                andamento += 1
            elif "CONCL" in s:
                concluido += 1
            elif "NEG" in s or "CANCEL" in s:
                negado += 1

        self.resumo.text = (
            f"EM ESPERA: {espera}   |   APROVADOS: {aprovado}\n"
            f"ANDAMENTO: {andamento}   |   CONCLUÍDOS: {concluido}\n"
            f"NEGADOS: {negado}   |   TOTAL: {len(orcamentos)}"
        )

    def buscar_cliente(self, instance=None):
        nome = self.busca.text.strip()

        if not nome:
            self.mostrar_mensagem("Digite o nome do cliente.")
            return

        try:
            orcamentos = buscar_orcamentos_por_cliente(nome)
            self.mostrar_orcamentos(orcamentos, f"BUSCA: {nome}")
        except Exception as erro:
            self.mostrar_mensagem(f"Erro na busca:\n{erro}")

    def mostrar_mensagem(self, texto):
        self.lista.clear_widgets()
        self.titulo.text = "RELATÓRIOS"

        self.lista.add_widget(Label(
            text=texto,
            color=(1, 1, 1, 1),
            font_size="15sp",
            size_hint_y=None,
            height=90
        ))

    def mostrar_orcamentos(self, orcamentos, titulo):
        self.lista.clear_widgets()
        self.titulo.text = f"{titulo} ({len(orcamentos)})"

        if not orcamentos:
            self.mostrar_mensagem("Nenhum orçamento encontrado.")
            return

        for orc in orcamentos:
            orc_id, cliente, valor, status, data = orc

            box = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None, height=116)

            texto = (
                f"Cliente: {cliente}\n"
                f"Orçamento: {orc_id} | Status: {status}\n"
                f"Valor: {self.moeda(valor)} | Data: {data}"
            )

            box.add_widget(Label(
                text=texto,
                color=(1, 1, 1, 1),
                font_size="14sp",
                bold=True,
                size_hint_y=None,
                height=70
            ))

            btn_abrir = Button(
                text="VISUALIZAR ORÇAMENTO",
                background_color=(0.75, 0, 0, 1),
                color=(1, 1, 1, 1),
                bold=True,
                size_hint_y=None,
                height=38
            )
            btn_abrir.bind(on_press=lambda instance, oid=orc_id: self.visualizar_orcamento(oid))

            box.add_widget(btn_abrir)
            self.lista.add_widget(box)

    def visualizar_orcamento(self, orcamento_id):
        self.lista.clear_widgets()

        dados = buscar_orcamento(orcamento_id)

        if not dados:
            self.mostrar_mensagem("Orçamento não encontrado.")
            return

        cliente = dados[1]
        telefone = dados[2] or "-"
        endereco = dados[3] or "-"
        status = dados[4]
        valor = dados[6]
        data = dados[7]

        self.titulo.text = f"ORÇAMENTO {orcamento_id}"

        self.lista.add_widget(Label(
            text=(
                f"CLIENTE: {cliente}\n"
                f"WHATSAPP: {telefone}\n"
                f"ENDEREÇO: {endereco}\n"
                f"STATUS: {status}\n"
                f"VALOR: {self.moeda(valor)}\n"
                f"DATA: {data}"
            ),
            color=(1, 1, 1, 1),
            font_size="14sp",
            bold=True,
            size_hint_y=None,
            height=150
        ))

        linha_status_1 = BoxLayout(spacing=5, size_hint_y=None, height=38)

        btn_aprovado = Button(text="APROVADO", background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), bold=True)
        btn_aprovado.bind(on_press=lambda instance, oid=orcamento_id: self.mudar_status(oid, "APROVADO"))

        btn_andamento = Button(text="ANDAMENTO", background_color=(0.8, 0.5, 0, 1), color=(1, 1, 1, 1), bold=True)
        btn_andamento.bind(on_press=lambda instance, oid=orcamento_id: self.mudar_status(oid, "EM ANDAMENTO"))

        linha_status_1.add_widget(btn_aprovado)
        linha_status_1.add_widget(btn_andamento)
        self.lista.add_widget(linha_status_1)

        linha_status_2 = BoxLayout(spacing=5, size_hint_y=None, height=38)

        btn_concluido = Button(text="CONCLUÍDO", background_color=(0, 0.4, 0.8, 1), color=(1, 1, 1, 1), bold=True)
        btn_concluido.bind(on_press=lambda instance, oid=orcamento_id: self.mudar_status(oid, "CONCLUÍDO"))

        btn_negado = Button(text="NEGADO", background_color=(0.4, 0.4, 0.4, 1), color=(1, 1, 1, 1), bold=True)
        btn_negado.bind(on_press=lambda instance, oid=orcamento_id: self.mudar_status(oid, "NEGADO"))

        linha_status_2.add_widget(btn_concluido)
        linha_status_2.add_widget(btn_negado)
        self.lista.add_widget(linha_status_2)

        itens = buscar_itens_orcamento(orcamento_id)

        for item in itens:
            item_id, tipo, descricao, largura, espessura, comprimento, quantidade, peso_kg, valor_total = item

            self.lista.add_widget(Label(
                text=(
                    f"{tipo} - {descricao}\n"
                    f"Corte: {largura} cm | Esp: {espessura}\n"
                    f"Comp: {comprimento} m | Qtd: {quantidade}\n"
                    f"Peso: {peso_kg} kg | Valor: {self.moeda(valor_total)}"
                ),
                color=(1, 1, 1, 1),
                font_size="14sp",
                size_hint_y=None,
                height=95
            ))

        btn_voltar_lista = Button(
            text="VOLTAR PARA RELATÓRIOS",
            background_color=(0.15, 0.15, 0.15, 1),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=None,
            height=50
        )
        btn_voltar_lista.bind(on_press=self.carregar_todos)
        self.lista.add_widget(btn_voltar_lista)

    def mudar_status(self, orcamento_id, novo_status):
        alterar_status_orcamento(orcamento_id, novo_status)
        self.visualizar_orcamento(orcamento_id)

    def voltar(self, instance):
        self.manager.current = "inicio"