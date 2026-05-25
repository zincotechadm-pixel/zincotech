import os
import webbrowser
from urllib.parse import quote

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from database import (
    listar_orcamentos,
    buscar_orcamentos_por_cliente,
    buscar_orcamento,
    buscar_cliente_por_nome,
    buscar_itens_orcamento,
    alterar_status_orcamento,
    excluir_orcamento
)

from pdf_generator import gerar_pdf_orcamento


class TelaServicos(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        principal = BoxLayout(orientation="vertical", padding=8, spacing=6)

        self.titulo = Label(
            text="SERVICOS / ORCAMENTOS",
            font_size="22sp",
            bold=True,
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=38
        )
        principal.add_widget(self.titulo)

        self.busca_cliente = TextInput(
            hint_text="Digite o nome do cliente",
            multiline=False,
            size_hint_y=None,
            height=42,
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(1, 0, 0, 1),
            padding=[10, 10, 10, 10]
        )
        principal.add_widget(self.busca_cliente)

        linha_busca = BoxLayout(spacing=5, size_hint_y=None, height=42)

        btn_buscar = Button(
            text="BUSCAR",
            background_color=(0.75, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True,
        )
        btn_buscar.bind(on_press=self.buscar_orcamentos)

        btn_todos = Button(
            text="MOSTRAR TODOS",
            background_color=(0.20, 0.20, 0.20, 1),
            color=(1, 1, 1, 1),
            bold=True,
        )
        btn_todos.bind(on_press=self.carregar_orcamentos)

        linha_busca.add_widget(btn_buscar)
        linha_busca.add_widget(btn_todos)
        principal.add_widget(linha_busca)

        scroll = ScrollView()

        self.lista = BoxLayout(
            orientation="vertical",
            spacing=8,
            size_hint_y=None
        )
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

        self.carregar_orcamentos()

    def on_pre_enter(self):
        self.carregar_orcamentos()

    def carregar_orcamentos(self, instance=None):
        self.busca_cliente.text = ""
        self.mostrar_orcamentos(listar_orcamentos(), "TODOS")

    def buscar_orcamentos(self, instance=None):
        nome = self.busca_cliente.text.strip()

        if not nome:
            self.mostrar_orcamentos([], "DIGITE UM NOME")
            return

        orcamentos = buscar_orcamentos_por_cliente(nome)
        self.mostrar_orcamentos(orcamentos, f"BUSCA: {nome}")

    def recarregar_tela_atual(self):
        if self.busca_cliente.text.strip():
            self.buscar_orcamentos()
        else:
            self.carregar_orcamentos()

    def mostrar_orcamentos(self, orcamentos, titulo):
        self.lista.clear_widgets()
        self.titulo.text = f"{titulo} ({len(orcamentos)})"

        if not orcamentos:
            self.lista.add_widget(Label(
                text="Nenhum orcamento encontrado.",
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=45
            ))
            return

        for orc in orcamentos:
            orc_id, cliente, valor, status, data = orc

            box = BoxLayout(
                orientation="vertical",
                spacing=4,
                size_hint_y=None,
                height=138
            )

            info = Label(
                text=f"#{orc_id} | {cliente}\nR$ {valor:.2f} | {status}\n{data}",
                color=(1, 1, 1, 1),
                font_size="14sp",
                bold=True,
                size_hint_y=None,
                height=58
            )
            box.add_widget(info)

            linha_acoes = BoxLayout(spacing=4, size_hint_y=None, height=34)

            btn_ver = self.botao("VER", (0.75, 0, 0, 1))
            btn_editar = self.botao("EDITAR", (0.55, 0, 0, 1))
            btn_pdf = self.botao("PDF", (0.10, 0.10, 0.10, 1))
            btn_whats = self.botao("WHATSAPP", (0, 0.55, 0.25, 1))

            btn_ver.bind(on_press=lambda instance, oid=orc_id: self.ver_itens(oid))
            btn_editar.bind(on_press=lambda instance, oid=orc_id, c=cliente: self.editar_orcamento(oid, c))
            btn_pdf.bind(on_press=lambda instance, oid=orc_id, c=cliente, v=valor, s=status, d=data: self.gerar_pdf(oid, c, v, s, d))
            btn_whats.bind(on_press=lambda instance, oid=orc_id, c=cliente: self.enviar_whatsapp(oid, c))

            linha_acoes.add_widget(btn_ver)
            linha_acoes.add_widget(btn_editar)
            linha_acoes.add_widget(btn_pdf)
            linha_acoes.add_widget(btn_whats)

            box.add_widget(linha_acoes)

            btn_excluir = Button(
                text="EXCLUIR ORCAMENTO",
                background_color=(0.45, 0, 0, 1),
                color=(1, 1, 1, 1),
                bold=True,
                size_hint_y=None,
                height=34
            )
            btn_excluir.bind(on_press=lambda instance, oid=orc_id: self.apagar_orcamento(oid))

            box.add_widget(btn_excluir)
            self.lista.add_widget(box)

    def botao(self, texto, cor):
        return Button(
            text=texto,
            background_color=cor,
            color=(1, 1, 1, 1),
            bold=True,
            font_size="11sp"
        )

    def editar_orcamento(self, orcamento_id, cliente):
        self.manager.current = "orcamentos"

        Clock.schedule_once(
            lambda dt: self.manager.get_screen("orcamentos").carregar_para_edicao(
                orcamento_id,
                cliente
            ),
            0
        )

    def gerar_pdf(self, orcamento_id, cliente, valor, status, data):
        arquivo = gerar_pdf_orcamento(
            orcamento_id,
            cliente,
            valor,
            status,
            data
        )

        print(f"PDF GERADO: {arquivo}")

        try:
            os.startfile(arquivo)
        except Exception as erro:
            print("Erro ao abrir PDF:", erro)

    def enviar_whatsapp(self, orcamento_id, cliente):
        dados = buscar_orcamento(orcamento_id)

        telefone = ""
        valor = 0

        if dados:
            telefone = "".join(
                numero for numero in (dados[2] or "")
                if numero.isdigit()
            )
            valor = dados[6] or 0

        # Se o orçamento antigo estiver sem telefone,
        # busca o telefone atualizado no cadastro do cliente.
        if not telefone:
            cliente_dados = buscar_cliente_por_nome(cliente)

            if cliente_dados:
                telefone = "".join(
                    numero for numero in (cliente_dados[2] or "")
                    if numero.isdigit()
                )

        if not telefone:
            print("Cliente sem telefone")
            return

        if not telefone.startswith("55"):
            telefone = "55" + telefone

        mensagem = (
            f"Olá {cliente}, seu orçamento ZINCOTECH "
            f"#{orcamento_id} está pronto.\n\n"
            f"Valor do orçamento: R$ {valor:.2f}\n\n"
            "O PDF foi gerado com sucesso."
        )

        link = f"https://wa.me/{telefone}?text={quote(mensagem)}"
        webbrowser.open(link)

        try:
            arquivo_pdf = f"orcamento_{orcamento_id}_{cliente.replace(' ', '_')}.pdf"

            caminho_pdf = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                arquivo_pdf
            )

            if os.path.exists(caminho_pdf):
                os.startfile(caminho_pdf)

        except Exception as erro:
            print("Erro PDF:", erro)

    def mudar_status(self, orcamento_id, status):
        alterar_status_orcamento(orcamento_id, status)
        self.recarregar_tela_atual()

    def apagar_orcamento(self, orcamento_id):
        excluir_orcamento(orcamento_id)
        self.recarregar_tela_atual()

    def ver_itens(self, orcamento_id):
        self.lista.clear_widgets()

        dados = buscar_orcamento(orcamento_id)

        cliente = dados[1] if dados else ""
        valor = dados[6] if dados else 0
        status = dados[4] if dados else ""
        data = dados[7] if dados else ""

        self.lista.add_widget(Label(
            text=f"ORCAMENTO #{orcamento_id}\n{cliente} | R$ {valor:.2f}\n{status} | {data}",
            color=(1, 0, 0, 1),
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height=80
        ))

        itens = buscar_itens_orcamento(orcamento_id)

        if not itens:
            self.lista.add_widget(Label(
                text="Nenhum item encontrado.",
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=40
            ))
        else:
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

                texto = (
                    f"{tipo} - {descricao}\n"
                    f"Corte: {largura} cm | Esp: {espessura}\n"
                    f"Comp: {comprimento} m | Qtd: {quantidade}\n"
                    f"Peso: {peso_kg} kg | R$ {valor_total:.2f}"
                )

                self.lista.add_widget(Label(
                    text=texto,
                    color=(1, 1, 1, 1),
                    font_size="14sp",
                    size_hint_y=None,
                    height=95
                ))

        btn_voltar_lista = Button(
            text="VOLTAR PARA LISTA",
            background_color=(0.15, 0.15, 0.15, 1),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=None,
            height=50
        )
        btn_voltar_lista.bind(on_press=self.carregar_orcamentos)

        self.lista.add_widget(btn_voltar_lista)

    def voltar(self, instance):
        self.manager.current = "inicio"