# -*- coding: utf-8 -*-
"""Lokal historiklagring i JSON."""

import json
from pathlib import Path


class HistoryStore:
    def __init__(self, app):
        self.path = Path(app.user_data_dir) / 'historik.json'

    def read(self):
        if not self.path.exists():
            return []
        try:
            return json.loads(self.path.read_text(encoding='utf-8'))
        except Exception:
            return []

    def write(self, items):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')

    def add(self, item):
        items = self.read()
        items.append(item)
        self.write(items)

    def clear(self):
        self.write([])
