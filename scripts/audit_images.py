import sys
from pathlib import Path

CARPETA_IMAGENES = "static"
LIMITE_KB = 500
FORMATOS_VALIDOS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".avif"}

errores = []
base = Path(CARPETA_IMAGENES)

if base.exists():
    for archivo in base.rglob("*"):
        if archivo.is_file():
            ext = archivo.suffix.lower()
            if ext not in FORMATOS_VALIDOS:
                continue
            size_kb = (archivo.stat().st_size + 1023) // 1024
            if size_kb > LIMITE_KB:
                errores.append((archivo, size_kb))

if errores:
    print("❌ Imágenes demasiado pesadas:\n", file=sys.stderr)
    for archivo, peso in errores:
        print(f"- {archivo} → {peso} KB (> 500 KB)", file=sys.stderr)
        print(f"::error file={archivo},title=Imagen pesada::Pesa {peso} KB", file=sys.stderr)
    sys.exit(1)
else:
    print("✅ Todas las imágenes cumplen el límite de 500 KB")
