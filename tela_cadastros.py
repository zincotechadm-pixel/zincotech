from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

from database import (
    adicionar_produto,
    listar_produtos,
    buscar_produtos,
    editar_produto,
    excluir_produto,
    salvar_configuracao,
    buscar_configuracao
)


class TelaCadastros(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.produto_editando_id = None

        principal = BoxLayout(orientation="vertical", padding=10, spacing=8)

        principal.add_widget(Label(
            text="CADASTROS / CONFIGURAÇÕES",
            font_size="22sp",
            bold=True,
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=42
        ))

        scroll = ScrollView()
        conteudo = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        conteudo.bind(minimum_height=conteudo.setter("height"))

        conteudo.add_widget(Label(
            text="PRODUTOS E ACESSÓRIOS",
            font_size="17sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=34
        ))

        self.nome = self.campo("Nome do produto")
        self.tipo = Spinner(
            text="UNIDADE",
            values=("UNIDADE", "KG", "METRO", "CAIXA"),
            size_hint_y=None,
            height=45
        )
        self.valor = self.campo("Valor de compra")
        self.lucro = self.campo("Lucro do produto %")

        self.valor.input_filter = "float"
        self.lucro.input_filter = "float"

        conteudo.add_widget(self.nome)
        conteudo.add_widget(self.tipo)
        conteudo.add_widget(self.valor)
        conteudo.add_widget(self.lucro)

        btn_salvar = Button(
            text="SALVAR PRODUTO",
            background_color=(0.75, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=None,
            height=50
        )
        btn_salvar.bind(on_press=self.salvar_produto)
        conteudo.add_widget(btn_salvar)

        conteudo.add_widget(Label(
            text="ALUMINIO",
            font_size="17sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=34
        ))

        self.preco_aluminio = self.campo("Valor que pago no KG do aluminio")
        self.lucro_aluminio = self.campo("Lucro do aluminio %")

        self.espessura_aluminio = Spinner(
            text=str(buscar_configuracao("espessura_aluminio") or "0.5"),
            values=("0.4", "0.5", "0.6", "0.7", "1.0"),
            size_hint_y=None,
            height=45
        )

        self.preco_aluminio.input_filter = "float"
        self.lucro_aluminio.input_filter = "float"
        self.preco_aluminio.text = str(buscar_configuracao("preco_kg_aluminio"))
        self.lucro_aluminio.text = str(buscar_configuracao("lucro_aluminio"))

        conteudo.add_widget(self.preco_aluminio)
        conteudo.add_widget(self.lucro_aluminio)

        conteudo.add_widget(Label(
            text="ESPESSURA DO ALUMÍNIO",
            font_size="14sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=26
        ))
        conteudo.add_widget(self.espessura_aluminio)

        btn_aluminio = Button(
            text="SALVAR ALUMINIO",
            background_color=(0.55, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=None,
            height=50
        )
        btn_aluminio.bind(on_press=self.salvar_aluminio)
        conteudo.add_widget(btn_aluminio)

        conteudo.add_widget(Label(
            text="CONFIGURAÇÃO DE MÃO DE OBRA",
            font_size="17sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=34
        ))

        self.mao_obra = self.campo("Mão de obra %")
        self.mao_obra.input_filter = "float"
        self.mao_obra.text = str(buscar_configuracao("mao_de_obra_percentual"))

        conteudo.add_widget(self.mao_obra)

        btn_mao_obra = Button(
            text="SALVAR MÃO DE OBRA",
            background_color=(0.55, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=None,
            height=50
        )
        btn_mao_obra.bind(on_press=self.salvar_mao_obra)
        conteudo.add_widget(btn_mao_obra)

        self.titulo_produtos = Label(
            text="PRODUTOS CADASTRADOS",
            font_size="17sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=34
        )
        conteudo.add_widget(self.titulo_produtos)

        self.busca_produto = self.campo("Buscar produto ou tipo")
        conteudo.add_widget(self.busca_produto)

        linha_busca = BoxLayout(spacing=5, size_hint_y=None, height=42)

        btn_buscar = Button(
            text="BUSCAR",
            background_color=(0.75, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_buscar.bind(on_press=self.buscar_produtos)

        btn_todos = Button(
            text="MOSTRAR TODOS",
            background_color=(0.20, 0.20, 0.20, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_todos.bind(on_press=self.carregar_produtos)

        linha_busca.add_widget(btn_buscar)
        linha_busca.add_widget(btn_todos)
        conteudo.add_widget(linha_busca)

        self.lista = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter("height"))

        conteudo.add_widget(self.lista)

        scroll.add_widget(conteudo)
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
        self.carregar_produtos()

    def campo(self, dica):
        return TextInput(
            hint_text=dica,
            multiline=False,
            size_hint_y=None,
            height=45,
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(1, 0, 0, 1),
            padding=[10, 10, 10, 10]
        )

    def salvar_produto(self, instance):
        nome = self.nome.text.strip()

        if not nome:
            print("Digite o nome do produto")
            return

        try:
            valor = float(self.valor.text)
            lucro = float(self.lucro.text)
        except:
            print("Digite valores válidos")
            return

        if self.produto_editando_id:
            editar_produto(
                self.produto_editando_id,
                nome,
                self.tipo.text,
                valor,
                lucro
            )
            self.produto_editando_id = None
        else:
            adicionar_produto(
                nome,
                self.tipo.text,
                valor,
                lucro
            )

        self.nome.text = ""
        self.valor.text = ""
        self.lucro.text = ""
        self.tipo.text = "UNIDADE"

        self.carregar_produtos()
        print("Produto salvo")

    def salvar_mao_obra(self, instance):
        salvar_configuracao(
            "mao_de_obra_percentual",
            self.mao_obra.text or 0
        )
        print("Mão de obra salva")

    def salvar_aluminio(self, instance):
        salvar_configuracao(
            "preco_kg_aluminio",
            self.preco_aluminio.text or 0
        )
        salvar_configuracao(
            "lucro_aluminio",
            self.lucro_aluminio.text or 0
        )
        salvar_configuracao(
            "espessura_aluminio",
            self.espessura_aluminio.text or 0.5
        )
        print("Aluminio salvo")

    def carregar_produtos(self, instance=None):
        self.busca_produto.text = ""
        self.mostrar_produtos(listar_produtos(), "PRODUTOS CADASTRADOS")

    def buscar_produtos(self, instance=None):
        termo = self.busca_produto.text.strip()

        if not termo:
            self.mostrar_produtos([], "DIGITE UM PRODUTO")
            return

        self.mostrar_produtos(buscar_produtos(termo), f"BUSCA: {termo}")

    def mostrar_produtos(self, produtos, titulo):
        self.lista.clear_widgets()
        self.titulo_produtos.text = f"{titulo} ({len(produtos)})"

        if not produtos:
            self.lista.add_widget(Label(
                text="Nenhum produto encontrado.",
                color=(0.8, 0.8, 0.8, 1),
                size_hint_y=None,
                height=40
            ))
            return

        for produto in produtos:
            produto_id, nome, tipo, valor, lucro = produto

            box = BoxLayout(orientation="vertical", spacing=5, size_hint_y=None, height=125)

            box.add_widget(Label(
                text=f"{nome} | {tipo}\nCompra: R$ {valor:.2f} | Lucro: {lucro}%",
                color=(1, 1, 1, 1),
                font_size="14sp",
                size_hint_y=None,
                height=45
            ))

            linha = BoxLayout(spacing=5, size_hint_y=None, height=42)

            btn_editar = Button(
                text="EDITAR",
                background_color=(0.75, 0, 0, 1),
                color=(1, 1, 1, 1),
                bold=True
            )
            btn_editar.bind(
                on_press=lambda instance, p=produto:
                self.preparar_edicao(p)
            )

            btn_excluir = Button(
                text="EXCLUIR",
                background_color=(0.25, 0.25, 0.25, 1),
                color=(1, 1, 1, 1),
                bold=True
            )
            btn_excluir.bind(
                on_press=lambda instance, pid=produto_id:
                self.apagar_produto(pid)
            )

            linha.add_widget(btn_editar)
            linha.add_widget(btn_excluir)

            box.add_widget(linha)
            self.lista.add_widget(box)

    def preparar_edicao(self, produto):
        produto_id, nome, tipo, valor, lucro = produto

        self.produto_editando_id = produto_id
        self.nome.text = nome
        self.tipo.text = tipo
        self.valor.text = str(valor)
        self.lucro.text = str(lucro)

        print("Editando produto:", nome)

    def apagar_produto(self, produto_id):
        excluir_produto(produto_id)
        if self.busca_produto.text.strip():
            self.buscar_produtos()
        else:
            self.carregar_produtos()

    def voltar(self, instance):
        self.manager.current = "inicio"