# -*- coding: utf-8 -*-
"""Mobilgränssnitt för Lönespec Pro Android v3.0."""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

from core.calculator import ERSATTNINGAR, berakna_lon, bygg_lonespec, format_kr, format_procent
from core.storage import HistoryStore


KV = r"""
#:import dp kivy.metrics.dp

<MoneyInput@TextInput>:
    multiline: False
    font_size: "18sp"
    size_hint_y: None
    height: dp(48)
    padding: [dp(12), dp(12), dp(12), dp(12)]
    background_normal: ""
    background_active: ""
    background_color: 1, 1, 1, 1
    foreground_color: 0.06, 0.09, 0.16, 1
    cursor_color: 0.15, 0.39, 0.92, 1

<Card@BoxLayout>:
    orientation: "vertical"
    padding: dp(14)
    spacing: dp(8)
    size_hint_y: None
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]

<BlueButton@Button>:
    size_hint_y: None
    height: dp(54)
    font_size: "18sp"
    bold: True
    background_normal: ""
    background_color: 0.15, 0.39, 0.92, 1
    color: 1, 1, 1, 1

<LightButton@Button>:
    size_hint_y: None
    height: dp(48)
    font_size: "16sp"
    background_normal: ""
    background_color: 0.89, 0.93, 0.98, 1
    color: 0.06, 0.09, 0.16, 1

<RootWidget>:
    orientation: "vertical"
    padding: dp(12)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: 0.97, 0.98, 0.99, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(64)
        orientation: "vertical"
        Label:
            text: "Lönespec Pro"
            color: 0.06, 0.09, 0.16, 1
            bold: True
            font_size: "27sp"
            halign: "left"
            valign: "middle"
            text_size: self.size
        Label:
            text: "Android v3.0 · Tabell 34 kolumn 1"
            color: 0.39, 0.45, 0.55, 1
            font_size: "13sp"
            halign: "left"
            valign: "middle"
            text_size: self.size

    ScrollView:
        do_scroll_x: False
        BoxLayout:
            orientation: "vertical"
            spacing: dp(12)
            size_hint_y: None
            height: self.minimum_height

            Card:
                height: self.minimum_height
                Label:
                    text: "Lön"
                    color: 0.06, 0.09, 0.16, 1
                    bold: True
                    font_size: "18sp"
                    size_hint_y: None
                    height: dp(28)
                    halign: "left"
                    text_size: self.size
                Label:
                    text: "Månadslön"
                    color: 0.39, 0.45, 0.55, 1
                    font_size: "14sp"
                    size_hint_y: None
                    height: dp(22)
                    halign: "left"
                    text_size: self.size
                MoneyInput:
                    id: manadslon
                    hint_text: "Skriv månadslön"
                    on_text: root.live_update()

            Card:
                height: self.minimum_height
                Label:
                    text: "Arbetade timmar"
                    color: 0.06, 0.09, 0.16, 1
                    bold: True
                    font_size: "18sp"
                    size_hint_y: None
                    height: dp(28)
                    halign: "left"
                    text_size: self.size
                GridLayout:
                    cols: 2
                    spacing: dp(8)
                    size_hint_y: None
                    height: self.minimum_height

                    Label:
                        text: "OB Enkel"
                        color: 0.06, 0.09, 0.16, 1
                        size_hint_y: None
                        height: dp(48)
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                    MoneyInput:
                        id: ob_enkel
                        hint_text: "0"
                        on_text: root.live_update()

                    Label:
                        text: "OB Kval"
                        color: 0.06, 0.09, 0.16, 1
                        size_hint_y: None
                        height: dp(48)
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                    MoneyInput:
                        id: ob_kval
                        hint_text: "0"
                        on_text: root.live_update()

                    Label:
                        text: "Övertid"
                        color: 0.06, 0.09, 0.16, 1
                        size_hint_y: None
                        height: dp(48)
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                    MoneyInput:
                        id: overtid
                        hint_text: "0"
                        on_text: root.live_update()

                    Label:
                        text: "Storhelg"
                        color: 0.06, 0.09, 0.16, 1
                        size_hint_y: None
                        height: dp(48)
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                    MoneyInput:
                        id: storhelg
                        hint_text: "0"
                        on_text: root.live_update()

                    Label:
                        text: "Storhelg högre"
                        color: 0.06, 0.09, 0.16, 1
                        size_hint_y: None
                        height: dp(48)
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                    MoneyInput:
                        id: storhelg_hogre
                        hint_text: "0"
                        on_text: root.live_update()

                    Label:
                        text: "Beredskap"
                        color: 0.06, 0.09, 0.16, 1
                        size_hint_y: None
                        height: dp(48)
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                    MoneyInput:
                        id: beredskap
                        hint_text: "0"
                        on_text: root.live_update()

            Card:
                height: self.minimum_height
                Label:
                    text: "Ersättningar"
                    color: 0.06, 0.09, 0.16, 1
                    bold: True
                    font_size: "18sp"
                    size_hint_y: None
                    height: dp(28)
                    halign: "left"
                    text_size: self.size
                Label:
                    text: root.ersattningar_text
                    color: 0.39, 0.45, 0.55, 1
                    font_size: "14sp"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(8)
                    halign: "left"
                    valign: "top"
                    text_size: self.width, None

            BlueButton:
                text: "Spara i historik"
                on_release: root.spara_aktuell()
            LightButton:
                text: "Historik"
                on_release: root.visa_historik()
            LightButton:
                text: "Rensa alla fält"
                on_release: root.rensa()

            Card:
                height: self.minimum_height
                Label:
                    text: "Sammanfattning"
                    color: 0.06, 0.09, 0.16, 1
                    bold: True
                    font_size: "18sp"
                    size_hint_y: None
                    height: dp(28)
                    halign: "left"
                    text_size: self.size
                Label:
                    text: root.summary_text
                    markup: True
                    color: 0.06, 0.09, 0.16, 1
                    font_size: "18sp"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(12)
                    halign: "left"
                    valign: "top"
                    text_size: self.width, None

            Card:
                height: self.minimum_height
                Label:
                    text: "Lönespecifikation"
                    color: 0.06, 0.09, 0.16, 1
                    bold: True
                    font_size: "18sp"
                    size_hint_y: None
                    height: dp(28)
                    halign: "left"
                    text_size: self.size
                Label:
                    text: root.spec_text
                    color: 0.06, 0.09, 0.16, 1
                    font_size: "13sp"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(12)
                    halign: "left"
                    valign: "top"
                    text_size: self.width, None
"""


class RootWidget(BoxLayout):
    summary_text = StringProperty('Brutto: 0 kr\nSkatt: 0 kr\nNetto: 0 kr')
    spec_text = StringProperty('Fyll i månadslön och timmar.')
    ersattningar_text = StringProperty('\n'.join([f'{namn}: {format_kr(v, 2)}/h' for namn, v in ERSATTNINGAR.items()]))

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        self.current_data = None
        self.store = None

    def on_kv_post(self, base_widget):
        app = App.get_running_app()
        self.store = HistoryStore(app)

    def _timmar_dict(self):
        return {
            'OB Enkel': self.ids.ob_enkel.text,
            'OB Kval': self.ids.ob_kval.text,
            'Övertid': self.ids.overtid.text,
            'Storhelg': self.ids.storhelg.text,
            'Storhelg högre': self.ids.storhelg_hogre.text,
            'Beredskap': self.ids.beredskap.text,
        }

    def live_update(self):
        if not hasattr(self, 'ids') or 'manadslon' not in self.ids:
            return
        data = berakna_lon(self.ids.manadslon.text, self._timmar_dict())
        self.current_data = data
        if not data:
            self.summary_text = 'Brutto: 0 kr\nSkatt: 0 kr\nNetto: 0 kr'
            self.spec_text = 'Fyll i månadslön och timmar.'
            return
        self.summary_text = (
            f"[b]Brutto:[/b] {format_kr(data['brutto'])}\n"
            f"[b]Skatt:[/b] -{format_kr(data['skatt'])}\n"
            f"[b]Netto:[/b] {format_kr(data['netto'])}\n"
            f"[b]Effektiv skatt:[/b] {format_procent(data['effektiv_skatt'])}"
        )
        self.spec_text = bygg_lonespec(data)

    def show_message(self, title, text):
        content = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        label = Label(text=text, halign='center', valign='middle')
        label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        content.add_widget(label)
        btn = Button(text='OK', size_hint_y=None, height=dp(46))
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.88, None), height=dp(260))
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def spara_aktuell(self):
        self.live_update()
        if not self.current_data:
            self.show_message('Saknad månadslön', 'Du måste fylla i månadslön innan du sparar.')
            return
        self.store.add(self.current_data)
        self.show_message('Sparad', 'Lönen har sparats i historiken.')

    def visa_historik(self):
        items = self.store.read() if self.store else []
        if not items:
            self.show_message('Historik', 'Ingen historik finns ännu.')
            return
        total_brutto = sum(item.get('brutto', 0) for item in items)
        total_skatt = sum(item.get('skatt', 0) for item in items)
        total_netto = sum(item.get('netto', 0) for item in items)
        lines = []
        lines.append(f'Antal sparade löner: {len(items)}')
        lines.append(f'Totalt brutto: {format_kr(total_brutto)}')
        lines.append(f'Totalt skatt: {format_kr(total_skatt)}')
        lines.append(f'Totalt netto: {format_kr(total_netto)}')
        lines.append('')
        lines.append('Senaste registreringar')
        lines.append('-' * 28)
        for item in reversed(items[-10:]):
            lines.append(
                f"{item.get('datum', '')}\n"
                f"Brutto: {format_kr(item.get('brutto', 0))}\n"
                f"Skatt: -{format_kr(item.get('skatt', 0))}\n"
                f"Netto: {format_kr(item.get('netto', 0))}\n"
            )
        self.show_message('Historik', '\n'.join(lines))

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
            field.text = ''
        self.current_data = None
        self.summary_text = 'Brutto: 0 kr\nSkatt: 0 kr\nNetto: 0 kr'
        self.spec_text = 'Fyll i månadslön och timmar.'
