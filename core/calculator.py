# -*- coding: utf-8 -*-
"""Beräkningsmotor för Lönespec Pro Android."""

from datetime import datetime
from core.tax import berakna_skatt

ERSATTNINGAR = {
    "OB Enkel": 24.57,
    "OB Kval": 54.96,
    "Övertid": 477.71,
    "Storhelg": 123.20,
    "Storhelg högre": 470.87,
    "Beredskap": 60.00,
}


def las_tal(v):
    try:
        text = str(v or '').strip().replace(' ', '').replace(',', '.')
        return float(text) if text else 0.0
    except Exception:
        return 0.0


def format_kr(v, decimaler=0):
    s = f"{v:,.{decimaler}f}"
    s = s.replace(',', 'X').replace('.', ',').replace('X', ' ')
    if decimaler == 0:
        s = s.split(',')[0]
    return f"{s} kr"


def format_procent(v):
    return f"{v:.1f}".replace('.', ',') + ' %'


def berakna_lon(manadslon_text, timmar_text):
    manadslon = las_tal(manadslon_text)
    if manadslon <= 0:
        return None

    poster = []
    brutto = manadslon
    totalt_timmar = 0.0

    for namn, ers in ERSATTNINGAR.items():
        timmar = las_tal(timmar_text.get(namn, ''))
        belopp = timmar * ers
        brutto += belopp
        totalt_timmar += timmar
        poster.append({'namn': namn, 'timmar': timmar, 'ersattning': ers, 'belopp': belopp})

    skatt = berakna_skatt(brutto)
    netto = brutto - skatt
    effektiv_skatt = (skatt / brutto * 100) if brutto else 0
    arslon = brutto * 12
    datum = datetime.now().strftime('%Y-%m-%d %H:%M')

    return {
        'datum': datum,
        'manadslon': manadslon,
        'poster': poster,
        'totalt_timmar': totalt_timmar,
        'brutto': brutto,
        'skatt': skatt,
        'netto': netto,
        'effektiv_skatt': effektiv_skatt,
        'arslon': arslon,
    }


def bygg_lonespec(data):
    if not data:
        return 'Fyll i månadslön och timmar.'

    lines = []
    lines.append('LÖNESPECIFIKATION')
    lines.append('=' * 36)
    lines.append(f"Datum: {data['datum']}")
    lines.append('Skatt: Tabell 34, kolumn 1')
    lines.append('')
    lines.append(f"Månadslön: {format_kr(data['manadslon'])}")
    lines.append('')
    lines.append('TILLÄGG')
    lines.append('-' * 36)

    for post in data['poster']:
        timmar_text = str(round(post['timmar'], 2)).replace('.', ',')
        ers_text = str(round(post['ersattning'], 2)).replace('.', ',')
        lines.append(f"{post['namn']}: {timmar_text} h × {ers_text} kr = {format_kr(post['belopp'])}")

    lines.append('')
    lines.append('-' * 36)
    lines.append(f"BRUTTO: {format_kr(data['brutto'])}")
    lines.append(f"SKATT: -{format_kr(data['skatt'])}")
    lines.append(f"NETTO: {format_kr(data['netto'])}")
    lines.append('')
    lines.append(f"Effektiv skatt: {format_procent(data['effektiv_skatt'])}")
    lines.append(f"Årslön: {format_kr(data['arslon'])}")
    return '\n'.join(lines)
