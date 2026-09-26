# Pasta Cleaner

Aplicación de escritorio para encontrar archivos duplicados, posibles versiones y elementos parecidos dentro de las carpetas que elijas.

## Cómo descargarlo

**Opción 1 — solo el ejecutable (recomendado si no vas a tocar el código):**
Andá a la sección [Releases](../../releases) del repositorio y descargá `PastaCleaner.exe` de la última versión.

**Opción 2 — todo el código fuente:**
Clic en el botón verde **Code** de este repositorio > **Download ZIP**, o si preferís por terminal:
git clone https://github.com/gustavobocuto/pastecleaner.git


## Cómo abrir el ejecutable

Doble clic en `PastaCleaner.exe`. Windows puede mostrar un aviso azul de SmartScreen ("Windows protegió su PC") porque el archivo no tiene firma digital — es normal en programas personales sin certificado pago. Para abrirlo igual: clic en **Más información** y después en **Ejecutar de todas formas**.

## Qué hace

- **Duplicados exactos** — mismo contenido (hash idéntico), sin importar el nombre o la carpeta.
- **Posibles versiones** — mismo nombre de archivo, contenido diferente. Útil para encontrar ese documento que guardaste en distintas carpetas.
- **Imágenes parecidas** — fotos visualmente similares, aunque cambie el tamaño o la compresión.
- **Textos parecidos** — archivos de texto con contenido muy cercano, no idéntico.

Nada se elimina sin confirmación. El borrado siempre muestra un resumen antes (cuántos archivos, cuánto espacio) y envía los archivos a la Papelera de reciclaje de Windows, nunca los borra directamente.

## Ejecutar el código
pip install -r requirements.txt
python main.py

## Generar el ejecutable (.exe)
build.bat

El ejecutable queda en `dist\PastaCleaner.exe`.

## Estructura

- `core/` — lógica de búsqueda y comparación, sin código de interfaz.
- `ui/` — ventana e interacción (PySide6).
- `main.py` — punto de entrada.
- `tests/` — pruebas de la lógica en `core/`.

# Pasta Cleaner

Desktop application to find duplicate files, possible versions, and similar items inside the folders you choose.

## How to get it

**Option 1 — just the executable (recommended if you're not touching the code):**
Go to the [Releases](../../releases) section of this repository and download `PastaCleaner.exe` from the latest release.

**Option 2 — full source code:**
Click the green **Code** button on this repository > **Download ZIP**, or via terminal:
git clone https://github.com/gustavobocuto/pastecleaner.git


## How to open the executable

Double-click `PastaCleaner.exe`. Windows may show a blue SmartScreen warning ("Windows protected your PC") because the file isn't digitally signed — normal for personal projects without a paid certificate. To open it anyway: click **More info**, then **Run anyway**.

## What it does

- **Exact duplicates** — identical content (same hash), regardless of name or folder.
- **Possible versions** — same file name, different content. Useful for finding that document you kept saving in different folders.
- **Similar images** — visually similar photos, even with different size or compression.
- **Similar text files** — text files with very close (not identical) content.

Nothing is deleted without confirmation. Deletion always shows a summary first (how many files, how much space) and sends files to the Windows Recycle Bin, never a direct delete.

## Running the code
pip install -r requirements.txt
python main.py


## Building the executable (.exe)
build.bat


The executable is generated at `dist\PastaCleaner.exe`.

## Structure

- `core/` — search and comparison logic, no UI code.
- `ui/` — window and interaction (PySide6).
- `main.py` — entry point.
- `tests/` — tests for the logic in `core/`.
