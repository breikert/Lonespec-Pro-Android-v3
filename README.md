# Lönespec Pro Android v3.0

Ny Android-grund för Lönespec Pro.

Windows-versionen v2.5 är fortfarande stabil huvudversion. Den här Android-versionen bygger vidare med en ny mobilanpassad struktur.

## Funktioner

- Mobilanpassad layout
- Automatisk beräkning medan du skriver
- Månadslön
- OB Enkel
- OB Kval
- Övertid
- Storhelg
- Storhelg högre
- Beredskap
- Skattetabell 34 kolumn 1
- Brutto, skatt, netto
- Lönespecifikation
- Lokal historik i JSON

## Projektstruktur

```text
main.py
core/
  calculator.py
  tax.py
  storage.py
ui/
  home.py
buildozer.spec
.github/workflows/build-apk.yml
```

## Bygga APK med GitHub Actions

1. Skapa ett nytt GitHub-repository.
2. Ladda upp hela innehållet i denna ZIP.
3. Gå till Actions.
4. Kör workflow: Build Android APK.
5. Ladda ner APK från artifacts när bygget lyckas.
