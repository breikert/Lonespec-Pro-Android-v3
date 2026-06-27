# -*- coding: utf-8 -*-
"""
Lönespec Pro Android v5.0
Designlyft:
- modernare kort/dashboard
- mindre scroll
- tydligare inputfält för timmar
- bottennavigering: Hem, Lönespec, Historik, Inställningar
- mörkt läge-grund
- versionsinfo flyttad till Inställningar
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.metrics import dp
from kivy.animation import Animation
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


def format_ersattning(v):
    return f"{v:.2f}".replace(".", ",") + " kr/h"


KV = r'''
#:import dp kivy.metrics.dp

<MoneyInput@TextInput>:
    multiline: False
    font_size: "16sp"
    size_hint_y: None
    height: dp(42)
    padding: [dp(12), dp(10), dp(12), dp(10)]
    background_normal: ""
    background_active: ""
    background_color: root.input_bg if hasattr(root, 'input_bg') else (1,1,1,1)
    foreground_color: root.text_color if hasattr(root, 'text_color') else (0.06,0.09,0.16,1)
    cursor_color: 0.15, 0.39, 0.92, 1

<Card@BoxLayout>:
    orientation: "vertical"
    padding: dp(12)
    spacing: dp(8)
    size_hint_y: None
    canvas.before:
        Color:
            rgba: app.root.card_color if app.root else (1, 1, 1, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(18)]

<SummaryCard@BoxLayout>:
    orientation: "vertical"
    padding: dp(10)
    spacing: dp(2)
    canvas.before:
        Color:
            rgba: app.root.card_color if app.root else (1, 1, 1, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(16)]

<BlueButton@Button>:
    size_hint_y: None
    height: dp(48)
    font_size: "15sp"
    bold: True
    background_normal: ""
    background_color: 0.15, 0.39, 0.92, 1
    color: 1, 1, 1, 1

<LightButton@Button>:
    size_hint_y: None
    height: dp(44)
    font_size: "14sp"
    background_normal: ""
    background_color: app.root.light_button_color if app.root else (0.89, 0.93, 0.98, 1)
    color: app.root.text_color if app.root else (0.06, 0.09, 0.16, 1)

<NavButton@Button>:
    size_hint_y: None
    height: dp(50)
    font_size: "13sp"
    background_normal: ""
    background_color: app.root.nav_color if app.root else (1,1,1,1)
    color: app.root.text_color if app.root else (0.06,0.09,0.16,1)

<SectionTitle@Label>:
    color: app.root.text_color if app.root else (0.06, 0.09, 0.16, 1)
    bold: True
    font_size: "18sp"
    size_hint_y: None
    height: dp(28)
    halign: "left"
    valign: "middle"
    text_size: self.size

<SmallLabel@Label>:
    color: app.root.muted_color if app.root else (0.39, 0.45, 0.55, 1)
    font_size: "12sp"
    size_hint_y: None
    height: dp(18)
    halign: "left"
    valign: "middle"
    text_size: self.size

RootWidget:
    orientation: "vertical"
    padding: dp(10)
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: root.bg_color
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(50)
        orientation: "vertical"
        Label:
            text: "Lönespec Pro"
            color: root.text_color
            bold: True
            font_size: "25sp"
            halign: "left"
            valign: "middle"
            text_size: self.size
        Label:
            text: "Android v5.0"
            color: root.muted_color
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
                color: root.muted_color
                font_size: "12sp"
                size_hint_y: None
                height: dp(20)
            Label:
                id: brutto_label
                text: root.brutto_text
                color: root.text_color
                bold: True
                font_size: "16sp"
        SummaryCard:
            Label:
                text: "Skatt"
                color: root.muted_color
                font_size: "12sp"
                size_hint_y: None
                height: dp(20)
            Label:
                id: skatt_label
                text: root.skatt_text
                color: 0.86, 0.15, 0.15, 1
                bold: True
                font_size: "16sp"
        SummaryCard:
            Label:
                text: "Netto"
                color: root.muted_color
                font_size: "12sp"
                size_hint_y: None
                height: dp(20)
            Label:
                id: netto_label
                text: root.netto_text
                color: 0.09, 0.64, 0.29, 1
                bold: True
                font_size: "16sp"

    Label:
        text: root.effektiv_skatt_text
        color: root.muted_color
        font_size: "14sp"
        size_hint_y: None
        height: dp(22)
        halign: "center"
        valign: "middle"
        text_size: self.size

    ScrollView:
        id: main_scroll
        do_scroll_x: False
        BoxLayout:
            id: content_box
            orientation: "vertical"
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height

            BoxLayout:
                id: page_home
                orientation: "vertical"
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                opacity: 1 if root.active_page == "home" else 0
                disabled: False if root.active_page == "home" else True

                Card:
                    height: self.minimum_height
                    SectionTitle:
                        text: "Månadslön"
                    MoneyInput:
                        id: manadslon
                        hint_text: "Skriv månadslön"
                        input_type: "number"
                        on_text: root.live_update()

                Card:
                    height: self.minimum_height
                    SectionTitle:
                        text: "Timmar"
                    GridLayout:
                        cols: 2
                        spacing: dp(8)
                        size_hint_y: None
                        height: self.minimum_height
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: dp(62)
                            SmallLabel:
                                text: "OB Enkel"
                            MoneyInput:
                                id: ob_enkel
                                hint_text: "0,0 h"
                                input_type: "number"
                                on_text: root.live_update()
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: dp(62)
                            SmallLabel:
                                text: "OB Kval"
                            MoneyInput:
                                id: ob_kval
                                hint_text: "0,0 h"
                                input_type: "number"
                                on_text: root.live_update()
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: dp(62)
                            SmallLabel:
                                text: "Övertid"
                            MoneyInput:
                                id: overtid
                                hint_text: "0,0 h"
                                input_type: "number"
                                on_text: root.live_update()
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: dp(62)
                            SmallLabel:
                                text: "Storhelg"
                            MoneyInput:
                                id: storhelg
                                hint_text: "0,0 h"
                                input_type: "number"
                                on_text: root.live_update()
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: dp(62)
                            SmallLabel:
                                text: "Storhelg högre"
                            MoneyInput:
                                id: storhelg_hogre
                                hint_text: "0,0 h"
                                input_type: "number"
                                on_text: root.live_update()
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: dp(62)
                            SmallLabel:
                                text: "Beredskap"
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

            BoxLayout:
                id: page_lonespec
                orientation: "vertical"
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height if root.active_page == "lonespec" else 0
                opacity: 1 if root.active_page == "lonespec" else 0
                disabled: False if root.active_page == "lonespec" else True
                Card:
                    height: dp(430)
                    SectionTitle:
                        text: "Lönespecifikation"
                    Label:
                        text: root.current_spec
                        color: root.text_color
                        font_size: "14sp"
                        halign: "left"
                        valign: "top"
                        text_size: self.size

            BoxLayout:
                id: page_history
                orientation: "vertical"
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height if root.active_page == "history" else 0
                opacity: 1 if root.active_page == "history" else 0
                disabled: False if root.active_page == "history" else True
                Card:
                    height: dp(430)
                    SectionTitle:
                        text: "Historik"
                    Label:
                        text: root.history_text
                        color: root.text_color
                        font_size: "14sp"
                        halign: "left"
                        valign: "top"
                        text_size: self.size

            BoxLayout:
                id: page_settings
                orientation: "vertical"
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height if root.active_page == "settings" else 0
                opacity: 1 if root.active_page == "settings" else 0
                disabled: False if root.active_page == "settings" else True
                Card:
                    height: self.minimum_height
                    SectionTitle:
                        text: "Inställningar"
                    SmallLabel:
                        text: "Skatt: Tabell 34, kolumn 1"
                    SmallLabel:
                        text: "Version: Android v5.0"
                    GridLayout:
                        cols: 2
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(44)
                        LightButton:
                            text: "Mörkt läge"
                            on_release: root.toggle_dark_mode()
                        LightButton:
                            text: "Ersättningar"
                            on_release: root.visa_ersattningar()

    GridLayout:
        cols: 4
        spacing: dp(6)
        size_hint_y: None
        height: dp(54)
        NavButton:
            text: "Hem"
            on_release: root.set_page("home")
        NavButton:
            text: "Lönespec"
            on_release: root.set_page("lonespec")
        NavButton:
            text: "Historik"
            on_release: root.set_page("history")
        NavButton:
            text: "Inställningar"
            on_release: root.set_page("settings")
'''


class RootWidget(BoxLayout):
    brutto_text = StringProperty("0 kr")
    skatt_text = StringProperty("0 kr")
    netto_text = StringProperty("0 kr")
    effektiv_skatt_text = StringProperty("Effektiv skatt: 0,0 %")
    current_spec = StringProperty("Fyll i månadslön och timmar.")
    history_text = StringProperty("Ingen historik finns ännu.")
    active_page = StringProperty("home")
    dark_mode = BooleanProperty(False)

    bg_color = ListProperty([0.97, 0.98, 0.99, 1])
    card_color = ListProperty([1, 1, 1, 1])
    text_color = ListProperty([0.06, 0.09, 0.16, 1])
    muted_color = ListProperty([0.39, 0.45, 0.55, 1])
    light_button_color = ListProperty([0.89, 0.93, 0.98, 1])
    nav_color = ListProperty([1, 1, 1, 1])
    input_bg = ListProperty([1, 1, 1, 1])

    ersattningar_text = StringProperty("\n".join([f"{namn}: {format_ersattning(v)}" for namn, v in ERSATTNINGAR.items()]))

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        self.current_data = None
        self.store = None

    def on_kv_post(self, base_widget):
        self.store = HistoryStore(App.get_running_app())
        self.update_history_text()

    def set_page(self, page):
        self.active_page = page
        if page == "lonespec":
            self.live_update()
        if page == "history":
            self.update_history_text()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.bg_color = [0.06, 0.08, 0.12, 1]
            self.card_color = [0.11, 0.14, 0.20, 1]
            self.text_color = [0.94, 0.96, 1, 1]
            self.muted_color = [0.65, 0.71, 0.80, 1]
            self.light_button_color = [0.18, 0.23, 0.31, 1]
            self.nav_color = [0.10, 0.13, 0.18, 1]
            self.input_bg = [0.15, 0.18, 0.24, 1]
        else:
            self.bg_color = [0.97, 0.98, 0.99, 1]
            self.card_color = [1, 1, 1, 1]
            self.text_color = [0.06, 0.09, 0.16, 1]
            self.muted_color = [0.39, 0.45, 0.55, 1]
            self.light_button_color = [0.89, 0.93, 0.98, 1]
            self.nav_color = [1, 1, 1, 1]
            self.input_bg = [1, 1, 1, 1]

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

        if "netto_label" in self.ids:
            anim = Animation(font_size="18sp", duration=0.08) + Animation(font_size="16sp", duration=0.10)
            anim.start(self.ids.netto_label)

    def show_message(self, title, text, height=320):
        content = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        label = Label(text=text, halign="left", valign="top", color=(0.06, 0.09, 0.16, 1))
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
        self.update_history_text()
        self.show_message("Sparad", "Lönen har sparats i historiken.", 230)

    def visa_ersattningar(self):
        self.show_message("Ersättningar", self.ersattningar_text, 340)

    def update_history_text(self):
        items = self.store.read() if self.store else []
        if not items:
            self.history_text = "Ingen historik finns ännu."
            return
        total_brutto = sum(item.get("brutto", 0) for item in items)
        total_skatt = sum(item.get("skatt", 0) for item in items)
        total_netto = sum(item.get("netto", 0) for item in items)
        lines = [
            f"Antal sparade löner: {len(items)}",
            f"Totalt brutto: {format_kr(total_brutto)}",
            f"Totalt skatt: {format_kr(total_skatt)}",
            f"Totalt netto: {format_kr(total_netto)}",
            "",
            "Senaste registreringar",
            "-" * 28,
        ]
        for item in reversed(items[-8:]):
            lines.append(f"{item.get('datum', '')}\nNetto: {format_kr(item.get('netto', 0))}\n")
        self.history_text = "\n".join(lines)

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
