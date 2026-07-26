import os
from src.database import get_card


class Deck:

    def __init__(self, decklist_path="decklist.txt"):
        self.decklist_path = decklist_path
        self.cards = []
        self.load_deck()

    def load_deck(self):
        if not os.path.exists(self.decklist_path):
            raise FileNotFoundError(
                f"No se encontró el archivo de mazo en {self.decklist_path}"
            )

        with open(self.decklist_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("//") or line.startswith("#"):
                continue

            # Procesar el formato típico "1 Nombre de Carta" o "Nombre de Carta"
            parts = line.split(" ", 1)
            if parts[0].isdigit():
                quantity = int(parts[0])
                card_name = parts[1].strip() if len(parts) > 1 else ""
            else:
                quantity = 1
                card_name = line.strip()

            if not card_name:
                continue

            # Obtener el objeto de carta mediante la base de datos
            card_obj = get_card(card_name)

            for _ in range(quantity):
                self.cards.append(card_obj)

    def get_cards(self):
        return self.cards

    def __len__(self):
        return len(self.cards)
