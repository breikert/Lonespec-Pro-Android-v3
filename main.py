# -*- coding: utf-8 -*-
"""Lönespec Pro Android v3.0."""

from kivy.app import App
from kivy.core.window import Window
from ui.home import RootWidget


class LonespecProApp(App):
    title = "Lönespec Pro"

    def build(self):
        Window.clearcolor = (0.97, 0.98, 0.99, 1)
        return RootWidget()


if __name__ == "__main__":
    LonespecProApp().run()
