from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from database import (
    adicionar_cliente,
    listar_clientes,
    buscar_clientes,
    editar_cliente,
    excluir_cliente
)


class TelaClientes(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cliente_editando_id = None

        principal = BoxLayout(orientation="vertical", padding=10, spacing=8)

        principal.add_widget(Label(
            text="CLIENTES",
            font_size="22sp",
            bold=True,
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=42
        ))

        self.nome = self.campo("Nome do cliente")
        self.telefone = self.campo("WhatsApp / Telefone")
        self.endereco = self.campo("Endereço")
        self.observacao = self.campo("Observação")

        principal.add_widget(self.nome)
        principal.add_widget(self.telefone)
        principal.add_widget(self.endereco)
        principal.add_widget(self.observacao)

        self.btn_salvar = Button(
            text="SALVAR CLIENTE",
            background_color=(0.75, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=None,
            height=50
        )
        self.btn_salvar.bind(on_press=self.salvar_cliente)
        principal.add_widget(self.btn_salvar)

        self.titulo_lista = Label(
            text="CLIENTES CADASTRADOS",
            font_size="17sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=35
        )
        principal.add_widget(self.titulo_lista)

        self.busca_cliente = self.campo("Buscar por nome, telefone ou endereco")
        principal.add_widget(self.busca_cliente)

        linha_busca = BoxLayout(spacing=5, size_hint_y=None, height=42)

        btn_buscar = Button(
            text="BUSCAR",
            background_color=(0.75, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_buscar.bind(on_press=self.buscar_clientes)

        btn_todos = Button(
            text="MOSTRAR TODOS",
            background_color=(0.20, 0.20, 0.20, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_todos.bind(on_press=self.carregar_clientes)

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

        self.carregar_clientes()

    def on_pre_enter(self):
        self.carregar_clientes()

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

    def salvar_cliente(self, instance):

        nome = self.nome.text.strip()

        if not nome:
            print("Digite o nome do cliente")
            return

        if self.cliente_editando_id:

            editar_cliente(
                self.cliente_editando_id,
                self.nome.text.strip(),
                self.telefone.text.strip(),
                self.endereco.text.strip(),
                self.observacao.text.strip()
            )

            print("Cliente atualizado")

            self.cliente_editando_id = None
            self.btn_salvar.text = "SALVAR CLIENTE"

        else:

            adicionar_cliente(
                self.nome.text.strip(),
                self.telefone.text.strip(),
                self.endereco.text.strip(),
                self.observacao.text.strip()
            )

            print("Cliente salvo")

        self.limpar_campos()
        self.carregar_clientes()

    def carregar_clientes(self, instance=None):
        self.busca_cliente.text = ""
        self.mostrar_clientes(
            listar_clientes(),
            "CLIENTES CADASTRADOS"
        )

    def buscar_clientes(self, instance=None):

        termo = self.busca_cliente.text.strip()

        if not termo:
            self.mostrar_clientes([], "DIGITE UM NOME")
            return

        self.mostrar_clientes(
            buscar_clientes(termo),
            f"BUSCA: {termo}"
        )

    def mostrar_clientes(self, clientes, titulo):

        self.lista.clear_widgets()

        self.titulo_lista.text = (
            f"{titulo} ({len(clientes)})"
        )

        if not clientes:

            self.lista.add_widget(Label(
                text="Nenhum cliente encontrado.",
                color=(0.8, 0.8, 0.8, 1),
                size_hint_y=None,
                height=40
            ))

            return

        for cliente in clientes:

            (
                cliente_id,
                nome,
                telefone,
                endereco,
                observacao,
                criado_em
            ) = cliente

            box = BoxLayout(
                orientation="vertical",
                spacing=5,
                size_hint_y=None,
                height=145
            )

            texto = (
                f"{nome}\n"
                f"WhatsApp: {telefone or ''}\n"
                f"Endereço: {endereco or ''}"
            )

            box.add_widget(Label(
                text=texto,
                color=(1, 1, 1, 1),
                font_size="14sp",
                size_hint_y=None,
                height=70
            ))

            linha = BoxLayout(
                spacing=5,
                size_hint_y=None,
                height=42
            )

            btn_editar = Button(
                text="EDITAR",
                background_color=(0.75, 0, 0, 1),
                color=(1, 1, 1, 1),
                bold=True
            )

            btn_editar.bind(
                on_press=lambda instance, c=cliente:
                self.preparar_edicao(c)
            )

            btn_excluir = Button(
                text="EXCLUIR",
                background_color=(0.25, 0.25, 0.25, 1),
                color=(1, 1, 1, 1),
                bold=True
            )

            btn_excluir.bind(
                on_press=lambda instance, cid=cliente_id:
                self.confirmar_exclusao(cid)
            )

            linha.add_widget(btn_editar)
            linha.add_widget(btn_excluir)

            box.add_widget(linha)

            self.lista.add_widget(box)

    def preparar_edicao(self, cliente):

        (
            cliente_id,
            nome,
            telefone,
            endereco,
            observacao,
            criado_em
        ) = cliente

        self.cliente_editando_id = cliente_id

        self.nome.text = nome
        self.telefone.text = telefone or ""
        self.endereco.text = endereco or ""
        self.observacao.text = observacao or ""

        self.btn_salvar.text = "SALVAR ALTERAÇÃO"

        print("Editando cliente:", nome)

    def confirmar_exclusao(self, cliente_id):

        box = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        texto = Label(
            text="Tem certeza que deseja excluir este cliente?",
            color=(1, 1, 1, 1)
        )

        linha = BoxLayout(
            spacing=10,
            size_hint_y=None,
            height=45
        )

        popup = Popup(
            title="CONFIRMAR EXCLUSÃO",
            content=box,
            size_hint=(0.85, 0.35),
            auto_dismiss=False
        )

        btn_sim = Button(
            text="SIM",
            background_color=(0.75, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True
        )

        btn_nao = Button(
            text="NÃO",
            background_color=(0.20, 0.20, 0.20, 1),
            color=(1, 1, 1, 1),
            bold=True
        )

        btn_sim.bind(
            on_press=lambda instance:
            self.apagar_cliente(cliente_id, popup)
        )

        btn_nao.bind(
            on_press=popup.dismiss
        )

        linha.add_widget(btn_sim)
        linha.add_widget(btn_nao)

        box.add_widget(texto)
        box.add_widget(linha)

        popup.open()

    def apagar_cliente(self, cliente_id, popup=None):

        excluir_cliente(cliente_id)

        if popup:
            popup.dismiss()

        if self.busca_cliente.text.strip():
            self.buscar_clientes()
        else:
            self.carregar_clientes()

        print("Cliente excluído")

    def limpar_campos(self):

        self.nome.text = ""
        self.telefone.text = ""
        self.endereco.text = ""
        self.observacao.text = ""

    def voltar(self, instance):
        self.manager.current = "inicio"