# -*- coding: utf-8 -*-
"""
Lönespec Pro Android v4.0 layout

Ny layout:
- Sammanfattning högst upp
- Kompakt tvåkolumnslayout för timmar
- Lönespecifikation i popup
- Ersättningar i popup
- Mindre scroll
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


KV = r"""
#:import dp kivy.metrics.dp

<MoneyInput@TextInput>:
    multiline: False
    font_size: "17sp"
    size_hint_y: None
    height: dp(44)
    padding: [dp(10), dp(10), dp(10), dp(10)]
    background_normal: ""
    background_active: ""
    background_color: 1, 1, 1, 1
    foreground_color: 0.06, 0.09, 0.16, 1
    cursor_color: 0.15, 0.39, 0.92, 1

<Card@BoxLayout>:
    orientation: "vertical"
    padding: dp(12)
    spacing: dp(7)
    size_hint_y: None
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(16)]

<SummaryCard@BoxLayout>:
    orientation: "vertical"
    padding: dp(8)
    spacing: dp(2)
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]

<BlueButton@Button>:
    size_hint_y: None
    height: dp(48)
    font_size: "16sp"
    bold: True
    background_normal: ""
    background_color: 0.15, 0.39, 0.92, 1
    color: 1, 1, 1, 1

<LightButton@Button>:
    size_hint_y: None
    height: dp(44)
    font_size: "15sp"
    background_normal: ""
    background_color: 0.89, 0.93, 0.98, 1
    color: 0.06, 0.09, 0.16, 1

<RootWidget>:
    orientation: "vertical"
    padding: dp(10)
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: 0.97, 0.98, 0.99, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(54)
        orientation: "vertical"
        Label:
            text: "Lönespec Pro"
            color: 0.06, 0.09, 0.16, 1
            bold: True
            font_size: "25sp"
            halign: "left"
            valign: "middle"
            text_size: self.size
        Label:
            text: "Android v4.0 · Tabell 34 kolumn 1"
            color: 0.39, 0.45, 0.55, 1
            font_size: "12sp"
            halign: "left"
            valign: "middle"
            text_size: self.size

    GridLayout:
        cols: 3
        spacing: dp(8)
        size_hint_y: None
        height: dp(78)

        SummaryCard:
            Label:
                text: "Brutto"
                color: 0.39, 0.45, 0.55, 1
                font_size: "12sp"
                size_hint_y: None
                height: dp(20)
            Label:
                text: root.brutto_text
                color: 0.06, 0.09, 0.16, 1
                bold: True
                font_size: "16sp"

        SummaryCard:
            Label:
                text: "Skatt"
                color: 0.39, 0.45, 0.55, 1
                font_size: "12sp"
                size_hint_y: None
                height: dp(20)
            Label:
                text: root.skatt_text
                color: 0.86, 0.15, 0.15, 1
                bold: True
                font_size: "16sp"

        SummaryCard:
            Label:
                text: "Netto"
                color: 0.39, 0.45, 0.55, 1
                font_size: "12sp"
                size_hint_y: None
                height: dp(20)
            Label:
                text: root.netto_text
                color: 0.09, 0.64, 0.29, 1
                bold: True
                font_size: "16sp"

    ScrollView:
        do_scroll_x: False

        BoxLayout:
            orientation: "vertical"
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height

            Card:
                height: self.minimum_height
                Label:
                    text: "Månadslön"
                    color: 0.06, 0.09, 0.16, 1
                    bold: True
                    font_size: "17sp"
                    size_hint_y: None
                    height: dp(26)
                    halign: "left"
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
                    color: 0.06, 0.09, 0.16, 1
                    bold: True
                    font_size: "17sp"
                    size_hint_y: None
                    height: dp(26)
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
                        height: dp(64)
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
                            hint_text: "0"
                            input_type: "number"
                            on_text: root.live_update()

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(64)
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
                            hint_text: "0"
                            input_type: "number"
                            on_text: root.live_update()

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(64)
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
                            hint_text: "0"
                            input_type: "number"
                            on_text: root.live_update()

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(64)
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
                            hint_text: "0"
                            input_type: "number"
                            on_text: root.live_update()

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(64)
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
                            hint_text: "0"
                            input_type: "number"
                            on_text: root.live_update()

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(64)
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
                            hint_text: "0"
                            input_type: "number"
                            on_text: root.live_update()

            Card:
                height: self.minimum_height
                Label:
                    text: root.extra_summary
                    markup: True
                    color: 0.06, 0.09, 0.16, 1
                    font_size: "15sp"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(4)
                    halign: "left"
                    valign: "top"
                    text_size: self.width, None

            GridLayout:
                cols: 2
                spacing: dp(8)
                size_hint_y: None
                height: dp(48)

                BlueButton:
                    text: "Spara"
                    on_release: root.spara_aktuell()

                LightButton:
                    text: "Lönespec"
                    on_release: root.visa_lonespec()

            GridLayout:
                cols: 3
                spacing: dp(8)
                size_hint_y: None
                height: dp(44)

                LightButton:
                    text: "Historik"
                    on_release: root.visa_historik()

                LightButton:
                    text: "Ersättning"
                    on_release: root.visa_ersattningar()

                LightButton:
                    text: "Rensa"
                    on_release: root.rensa()
"""


class RootWidget(BoxLayout):
    brutto_text = StringProperty("0 kr")
    skatt_text = StringProperty("0 kr")
    netto_text = StringProperty("0 kr")
    extra_summary = StringProperty("Fyll i månadslön och timmar. Resultatet uppdateras automatiskt.")
    ersattningar_text = StringProperty(
        "\\n".join([f"{namn}: {format_kr(v, 2)}/h" for namn, v in ERSATTNINGAR.items()])
    )

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
            self.extra_summary = "Fyll i månadslön och timmar. Resultatet uppdateras automatiskt."
            self.current_spec = "Fyll i månadslön och timmar."
            return

        self.brutto_text = format_kr(data["brutto"])
        self.skatt_text = "-" + format_kr(data["skatt"])
        self.netto_text = format_kr(data["netto"])
        self.extra_summary = (
            f"[b]Effektiv skatt:[/b] {format_procent(data['effektiv_skatt'])}\\n"
            f"[b]Totalt timmar:[/b] {str(round(data['totalt_timmar'], 2)).replace('.', ',')} h\\n"
            f"[b]Årslön:[/b] {format_kr(data['arslon'])}"
        )
        self.current_spec = bygg_lonespec(data)

    def show_message(self, title, text, height=320):
        content = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        label = Label(text=text, halign="left", valign="top")
        label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        content.add_widget(label)

        btn = Button(text="OK", size_hint_y=None, height=dp(44))
        content.add_widget(btn)

        popup = Popup(title=title, content=content, size_hint=(0.92, None), height=dp(height))
        btn.bind(on_release=popup.dismiss)
        popup.open()

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
                f"{item.get('datum', '')}\\n"
                f"Netto: {format_kr(item.get('netto', 0))}\\n"
            )

        self.show_message("Historik", "\\n".join(lines), 620)

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
        self.extra_summary = "Fyll i månadslön och timmar. Resultatet uppdateras automatiskt."
