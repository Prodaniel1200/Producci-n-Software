import csv
from pathlib import Path

FIELDNAMES = ["email", "password", "name"]


class UserRepository:
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.csv_path.exists():
            with self.csv_path.open("w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
                writer.writeheader()

    def list_users(self):
        with self.csv_path.open(newline="", encoding="utf-8") as csvfile:
            return list(csv.DictReader(csvfile))

    def get_by_email(self, email: str):
        for user in self.list_users():
            if user["email"] == email:
                return user
        return None

    def create(self, user_data: dict):
        with self.csv_path.open("a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(user_data)
