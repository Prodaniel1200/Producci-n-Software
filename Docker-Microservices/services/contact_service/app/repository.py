import csv
from pathlib import Path

FIELDNAMES = ["Nombre", "Correo", "Asunto", "Mensaje"]


class ContactRepository:
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, nombre: str, correo: str, asunto: str, mensaje: str):
        exists = self.csv_path.exists()
        with self.csv_path.open("a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if not exists:
                writer.writerow(FIELDNAMES)
            writer.writerow([nombre, correo, asunto, mensaje])
