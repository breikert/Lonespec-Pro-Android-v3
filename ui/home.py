# -*- coding: utf-8 -*-
"""
Lönespec Pro Android v5.0

Stabil UI-uppdatering byggd ovanpå den fungerande v4.1-koden.
Fokus:
- Modernare kort och tydligare startsida.
- Mindre scroll och kompaktare inmatning.
- Tydligare knapphierarki med Spara som huvudknapp.
- Bottennavigation med Hem, Historik, Lönespec och Inställningar.
- Versionsinfo flyttad till Inställningar/Om appen.
- Samma id:n och samma beräkningslogik som tidigare för att minimera kraschrisken.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

from core.calculator import (
    ERSATTNINGAR,
    berakna_lon,
    bygg_lonespec,
    format_kr,
    format_procent,
)
from core.storage import HistoryStore


APP_VERSION = "Android v5.0"
APP_INFO = "Lönespec Pro Android v5.0\nBygger vidare på den stabila v4.1-versionen."


def format_ersattning(v):
    """Visar ersättning snyggt, t.ex. 24,57 kr/h."""
    return f"{v:.2f}".replace(".", ",") + " kr/h"


KV = r"""
#:import dp kivy.metrics.dp

<MoneyInput@TextInput>:
    multiline: False
    font_size: "16sp"
    size_hint_y: None
    height: dp(40)
    padding: [dp(10), dp(8), dp(10), dp(8)]
    background_normal: ""
    background_active: ""
    background_color: 0.96, 0.98, 1, 1
    foreground_color: 0.05, 0.08, 0.14, 1
    cursor_color: 0.13, 0.34, 0.78, 1

<Card@BoxLayout>:
    orientation: "vertical"
    padding: dp(12)
    spacing: dp(7)
    size_hint_y: None
    canvas.before:
        Color:
            rgba: 0.88, 0.91, 0.95, 1
        RoundedRectangle:
            pos: self.x, self.y - dp(1)
            size: self.size
            radius: [dp(18)]
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(18)]

<SummaryCard@BoxLayout>:
    orientation: "vertical"
    padding: dp(9)
    spacing: dp(1)
    canvas.before:
        Color:
            rgba: 0.88, 0.91, 0.95, 1
        RoundedRectangle:
            pos: self.x, self.y - dp(1)
            size: self.size
            radius: [dp(16)]
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(16)]

<BlueButton@Button>:
    size_hint_y: None
    height: dp(48)
    font_size: "16sp"
    bold: True
    background_normal: ""
    background_down: ""
    background_color: 0.13, 0.34, 0.78, 1
    color: 1, 1, 1, 1

<LightButton@Button>:
    size_hint_y: None
    height: dp(44)
    font_size: "14sp"
    background_normal: ""
    background_down: ""
    background_color: 0.91, 0.95, 1, 1
    color: 0.05, 0.08, 0.14, 1

<NavButton@Button>:
    size_hint_y: None
    height: dp(52)
    font_size: "13sp"
    background_normal: ""
    background_down: ""
    background_color: 0.98, 0.99, 1, 1
    color: 0.13, 0.34, 0.78, 1

<RootWidget>:
    orientation: "vertical"
    padding: [dp(10), dp(8), dp(10), dp(6)]
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: 0.95, 0.97, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(42)
        orientation: "vertical"
        Label:
            text: "Lönespec Pro"
            color: 0.05, 0.08, 0.14, 1
            bold: True
            font_size: "25sp"
            halign: "left"
            valign: "middle"
            text_size: self.size
        Label:
            text: "Snabb översikt över din lön"
            color: 0.39, 0.45, 0.55, 1
            font_size: "12sp"
            halign: "left"
            valign: "middle"
            text_size: self.size

    GridLayout:
        cols: 3
        spacing: dp(8)
        size_hint_y: None
        height: dp(82)

        SummaryCard:
            Label:
                text: "Brutto"
                color: 0.39, 0.45, 0.55, 1
                font_size: "12sp"
                size_hint_y: None
                height: dp(20)
            Label:
                text: root.brutto_text
                color: 0.05, 0.08, 0.14, 1
                bold: True
                font_size: "16sp"
                halign: "center"
                text_size: self.size

        SummaryCard:
            Label:
                text: "Skatt"
                color: 0.39, 0.45, 0.55, 1
                font_size: "12sp"
                size_hint_y: None
                height: dp(20)
            Label:
                text: root.skatt_text
                color: 0.82, 0.14, 0.14, 1
                bold: True
                font_size: "16sp"
                halign: "center"
                text_size: self.size

        SummaryCard:
            Label:
                text: "Netto"
                color: 0.39, 0.45, 0.55, 1
                font_size: "12sp"
                size_hint_y: None
                height: dp(20)
            Label:
                text: root.netto_text
                color: 0.07, 0.56, 0.28, 1
                bold: True
                font_size: "16sp"
                halign: "center"
                text_size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(28)
        padding: [dp(8), 0, dp(8), 0]
        canvas.before:
            Color:
                rgba: 0.88, 0.94, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(14)]
        Label:
            text: root.effektiv_skatt_text
            color: 0.13, 0.34, 0.78, 1
            bold: True
            font_size: "13sp"
            halign: "center"
            valign: "middle"
            text_size: self.size

    ScrollView:
        do_scroll_x: False

        BoxLayout:
            orientation: "vertical"
            spacing: dp(9)
            size_hint_y: None
            height: self.minimum_height

            Card:
                height: dp(92)
                BoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: dp(25)
                    Label:
                        text: "Månadslön"
                        color: 0.05, 0.08, 0.14, 1
                        bold: True
                        font_size: "17sp"
                        halign: "left"
                        text_size: self.size
                    Label:
                        text: "kr före skatt"
                        color: 0.39, 0.45, 0.55, 1
                        font_size: "12sp"
                        halign: "right"
                        text_size: self.size
                MoneyInput:
                    id: manadslon
                    hint_text: "Skriv månadslön"
                    input_type: "number"
                    on_text: root.live_update()

            Card:
                height: self.minimum_height
                Label:
                    text: "Timmar"
                    color: 0.05, 0.08, 0.14, 1
                    bold: True
                    font_size: "17sp"
                    size_hint_y: None
                    height: dp(25)
                    halign: "left"
                    text_size: self.size

                GridLayout:
                    cols: 2
                    spacing: dp(8)
                    size_hint_y: None
                    height: self.minimum_height

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(60)
                        Label:
                            text: "OB Enkel"
                            color: 0.39, 0.45, 0.55, 1
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(18)
                            halign: "left"
                            text_size: self.size
                        MoneyInput:
                            id: ob_enkel
                            hint_text: "0,0 h"
                            input_type: "number"
                            on_text: root.live_update()

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(60)
                        Label:
                            text: "OB Kval"
                            color: 0.39, 0.45, 0.55, 1
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(18)
                            halign: "left"
                            text_size: self.size
                        MoneyInput:
                            id: ob_kval
                            hint_text: "0,0 h"
                            input_type: "number"
                            on_text: root.live_update()

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(60)
                        Label:
                            text: "Övertid"
                            color: 0.39, 0.45, 0.55, 1
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(18)
                            halign: "left"
                            text_size: self.size
                        MoneyInput:
                            id: overtid
                            hint_text: "0,0 h"
                            input_type: "number"
                            on_text: root.live_update()

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(60)
                        Label:
                            text: "Storhelg"
                            color: 0.39, 0.45, 0.55, 1
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(18)
                            halign: "left"
                            text_size: self.size
                        MoneyInput:
                            id: storhelg
                            hint_text: "0,0 h"
                            input_type: "number"
                            on_text: root.live_update()

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(60)
                        Label:
                            text: "Storhelg högre"
                            color: 0.39, 0.45, 0.55, 1
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(18)
                            halign: "left"
                            text_size: self.size
                        MoneyInput:
                            id: storhelg_hogre
                            hint_text: "0,0 h"
                            input_type: "number"
                            on_text: root.live_update()

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(60)
                        Label:
                            text: "Beredskap"
                            color: 0.39, 0.45, 0.55, 1
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(18)
                            halign: "left"
                            text_size: self.size
                        MoneyInput:
                            id: beredskap
                            hint_text: "0,0 h"
                            input_type: "number"
                            on_text: root.live_update()

            GridLayout:
                cols: 2
                spacing: dp(8)
                size_hint_y: None
                height: dp(48)

                BlueButton:
                    text: "Spara"
                    on_release: root.spara_aktuell()

                LightButton:
                    text: "Rensa"
                    on_release: root.rensa()

    GridLayout:
        cols: 4
        spacing: dp(4)
        size_hint_y: None
        height: dp(54)
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(18)]

        NavButton:
            text: "Hem"
            on_release: root.go_home()
        NavButton:
            text: "Historik"
            on_release: root.visa_historik()
        NavButton:
            text: "Lönespec"
            on_release: root.visa_lonespec()
        NavButton:
            text: "Mer"
            on_release: root.visa_installningar()
"""


class RootWidget(BoxLayout):
    brutto_text = StringProperty("0 kr")
    skatt_text = StringProperty("0 kr")
    netto_text = StringProperty("0 kr")
    effektiv_skatt_text = StringProperty("Effektiv skatt: 0,0 %")
    ersattningar_text = StringProperty("\n".join([f"{namn}: {format_ersattning(v)}" for namn, v in ERSATTNINGAR.items()]))

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        self.current_data = None
        self.current_spec = "Fyll i månadslön och timmar."
        self.store = None

    def on_kv_post(self, base_widget):
        self.store = HistoryStore(App.get_running_app())

    def _timmar_dict(self):
        return {
            "OB Enkel": self.ids.ob_enkel.text,
            "OB Kval": self.ids.ob_kval.text,
            "Övertid": self.ids.overtid.text,
            "Storhelg": self.ids.storhelg.text,
            "Storhelg högre": self.ids.storhelg_hogre.text,
            "Beredskap": self.ids.beredskap.text,
        }

    def live_update(self):
        if not hasattr(self, "ids") or "manadslon" not in self.ids:
            return

        data = berakna_lon(self.ids.manadslon.text, self._timmar_dict())
        self.current_data = data

        if not data:
            self.brutto_text = "0 kr"
            self.skatt_text = "0 kr"
            self.netto_text = "0 kr"
            self.effektiv_skatt_text = "Effektiv skatt: 0,0 %"
            self.current_spec = "Fyll i månadslön och timmar."
            return

        self.brutto_text = format_kr(data["brutto"])
        self.skatt_text = "-" + format_kr(data["skatt"])
        self.netto_text = format_kr(data["netto"])
        self.effektiv_skatt_text = f"Effektiv skatt: {format_procent(data['effektiv_skatt'])}"
        self.current_spec = bygg_lonespec(data)

    def show_message(self, title, text, height=320):
        content = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        label = Label(text=text, halign="left", valign="top", color=(0.05, 0.08, 0.14, 1))
        label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        content.add_widget(label)

        btn = Button(
            text="OK",
            size_hint_y=None,
            height=dp(44),
            background_normal="",
            background_color=(0.13, 0.34, 0.78, 1),
            color=(1, 1, 1, 1),
        )
        content.add_widget(btn)

        popup = Popup(title=title, content=content, size_hint=(0.92, None), height=dp(height))
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def go_home(self):
        self.live_update()

    def spara_aktuell(self):
        self.live_update()

        if not self.current_data:
            self.show_message("Saknad månadslön", "Du måste fylla i månadslön innan du sparar.", 230)
            return

        self.store.add(self.current_data)
        self.show_message("Sparad", "Lönen har sparats i historiken.", 230)

    def visa_lonespec(self):
        self.live_update()
        self.show_message("Lönespecifikation", self.current_spec, 620)

    def visa_ersattningar(self):
        self.show_message("Ersättningar", self.ersattningar_text, 360)

    def visa_installningar(self):
        text = (
            "Inställningar\n"
            "- Mörkt läge: förbereds i nästa steg\n"
            "- Egna lönearter: planerat\n"
            "- Export till PDF: planerat\n\n"
            "Om appen\n"
            f"{APP_INFO}\n\n"
            "Ersättningar finns under knappen nedan."
        )

        content = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(8))
        label = Label(text=text, halign="left", valign="top", color=(0.05, 0.08, 0.14, 1))
        label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        content.add_widget(label)

        btn_rates = Button(
            text="Visa ersättningar",
            size_hint_y=None,
            height=dp(44),
            background_normal="",
            background_color=(0.91, 0.95, 1, 1),
            color=(0.05, 0.08, 0.14, 1),
        )
        btn_close = Button(
            text="Stäng",
            size_hint_y=None,
            height=dp(44),
            background_normal="",
            background_color=(0.13, 0.34, 0.78, 1),
            color=(1, 1, 1, 1),
        )
        content.add_widget(btn_rates)
        content.add_widget(btn_close)

        popup = Popup(title="Mer", content=content, size_hint=(0.92, None), height=dp(520))
        btn_close.bind(on_release=popup.dismiss)
        btn_rates.bind(on_release=lambda *_: (popup.dismiss(), self.visa_ersattningar()))
        popup.open()

    def visa_historik(self):
        items = self.store.read() if self.store else []

        if not items:
            self.show_message("Historik", "Ingen historik finns ännu.", 230)
            return

        total_brutto = sum(item.get("brutto", 0) for item in items)
        total_skatt = sum(item.get("skatt", 0) for item in items)
        total_netto = sum(item.get("netto", 0) for item in items)

        lines = []
        lines.append(f"Antal sparade löner: {len(items)}")
        lines.append(f"Totalt brutto: {format_kr(total_brutto)}")
        lines.append(f"Totalt skatt: {format_kr(total_skatt)}")
        lines.append(f"Totalt netto: {format_kr(total_netto)}")
        lines.append("")
        lines.append("Senaste registreringar")
        lines.append("-" * 28)

        for item in reversed(items[-8:]):
            lines.append(
                f"{item.get('datum', '')}\n"
                f"Brutto: {format_kr(item.get('brutto', 0))}\n"
                f"Skatt: {format_kr(item.get('skatt', 0))}\n"
                f"Netto: {format_kr(item.get('netto', 0))}\n"
            )

        self.show_message("Historik", "\n".join(lines), 620)

    def rensa(self):
        for field in [
            self.ids.manadslon,
            self.ids.ob_enkel,
            self.ids.ob_kval,
            self.ids.overtid,
            self.ids.storhelg,
            self.ids.storhelg_hogre,
            self.ids.beredskap,
        ]:
            field.text = ""

        self.current_data = None
        self.current_spec = "Fyll i månadslön och timmar."
        self.brutto_text = "0 kr"
        self.skatt_text = "0 kr"
        self.netto_text = "0 kr"
        self.effektiv_skatt_text = "Effektiv skatt: 0,0 %"
