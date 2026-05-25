import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from tela_cadastros import TelaCadastros
from tela_clientes import TelaClientes
from tela_orcamentos import TelaOrcamentos
from tela_servicos import TelaServicos
from tela_relatorios import TelaRelatorios


PASTAS = [
    "dados",
    "pdfs",
    "pdfs/orcamentos",
    "imagens",
    "imagens/logos",
    "backups"
]

for pasta in PASTAS:
    os.makedirs(pasta, exist_ok=True)


Window.size = (360, 660)
Window.clearcolor = (0, 0, 0, 1)


class Home(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        fundo = Image(
            source="fundo_home.png",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            allow_stretch=True,
            keep_ratio=False
        )

        layout.add_widget(fundo)

        self.criar_botao(layout, "ORÇAMENTOS", 0.08, 0.41, 0.40, 0.20)
        self.criar_botao(layout, "SERVIÇOS", 0.52, 0.41, 0.40, 0.20)
        self.criar_botao(layout, "CLIENTES", 0.08, 0.18, 0.40, 0.20)
        self.criar_botao(layout, "RELATÓRIOS", 0.52, 0.18, 0.40, 0.20)

        self.criar_botao(layout, "INICIO", 0.00, 0.00, 0.20, 0.13)
        self.criar_botao(layout, "MENU_ORCAMENTO", 0.20, 0.00, 0.22, 0.13)
        self.criar_botao(layout, "NOVO", 0.42, 0.00, 0.16, 0.14)
        self.criar_botao(layout, "MENU_CLIENTES", 0.58, 0.00, 0.22, 0.13)
        self.criar_botao(layout, "CONFIG", 0.80, 0.00, 0.20, 0.13)

        self.add_widget(layout)

    def criar_botao(self, layout, nome, x, y, w, h):

        btn = Button(
            text="",
            background_color=(0, 0, 0, 0),
            size_hint=(w, h),
            pos_hint={"x": x, "y": y}
        )

        def clique(instance):
            print(f"Clicou em: {nome}")

            if nome == "CONFIG":
                self.manager.current = "cadastros"

            elif nome == "CLIENTES":
                self.manager.current = "clientes"

            elif nome == "MENU_CLIENTES":
                self.manager.current = "clientes"

            elif nome == "ORÇAMENTOS":
                self.manager.current = "orcamentos"

            elif nome == "MENU_ORCAMENTO":
                self.manager.current = "orcamentos"

            elif nome == "NOVO":
                self.manager.current = "orcamentos"

            elif nome == "SERVIÇOS":
                self.manager.current = "servicos"

            elif nome == "RELATÓRIOS":
                self.manager.current = "relatorios"

            elif nome == "INICIO":
                self.manager.current = "inicio"

        btn.bind(on_press=clique)
        layout.add_widget(btn)


class ZincotechApp(App):

    def build(self):

        sm = ScreenManager()

        sm.add_widget(Home(name="inicio"))
        sm.add_widget(TelaCadastros(name="cadastros"))
        sm.add_widget(TelaClientes(name="clientes"))
        sm.add_widget(TelaOrcamentos(name="orcamentos"))
        sm.add_widget(TelaServicos(name="servicos"))
        sm.add_widget(TelaRelatorios(name="relatorios"))

        return sm


if __name__ == "__main__":
    ZincotechApp().run()