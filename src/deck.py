import os
import re
from src.card import Card
from src.database import get_card


class Deck:
    """Handles loading, parsing, and managing the 99-card Commander library."""

    def __init__(self, filepath: str = "decklist.txt"):
        self.filepath = filepath
        self.cards = []
        self.other_cards = []  # Tracks unique cards categorized as OTHER
        self.load_deck()

    def load_deck(self):
        """Reads decklist.txt, parses quantities/names, and maps them to Card objects."""
        self.cards = []
        self.other_cards = []

        if not os.path.exists(self.filepath):
            print(
                f"Warning: {self.filepath} not found. Initializing empty deck."
            )
            return

        with open(self.filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            # Ignore empty lines or comments starting with # or //
            if not line or line.startswith("#") or line.startswith("//"):
                continue

            # Parse lines like "1 Sol Ring", "1x Sol Ring", or just "Sol Ring"
            match = re.match(r"^(?:(\d+)\s*x?\s+)?(.+)$", line, re.IGNORECASE)
            if match:
                qty = int(match.group(1)) if match.group(1) else 1
                raw_name = match.group(2).strip()

                # Clean set codes or collector numbers (e.g. "Sol Ring (CMR) 310")
                card_name = re.sub(r"\s*\([^)]*\).*", "", raw_name).strip()

                card_obj = get_card(card_name)

                # Track if card is not configured in database.py
                if card_obj.role == "Other" or card_obj.name == "OTHER":
                    if card_name not in self.other_cards:
                        self.other_cards.append(card_name)

                for _ in range(qty):
                    self.cards.append(card_obj)

        # Pad remaining deck slots up to 99 with filler cards if the list has fewer entries
        target_size = 99
        if len(self.cards) < target_size:
            missing = target_size - len(self.cards)
            for _ in range(missing):
                self.cards.append(
                    Card(name="OTHER", card_type="Unknown", role="Other")
                )

        # Output parser summary to terminal
        self._print_other_summary()

    def _print_other_summary(self):
        """Prints a summary notice showing cards categorized as 'OTHER'."""
        if self.other_cards:
            print("\n" + "=" * 55)
            print("ℹ️  DECK PARSER NOTICE: Unconfigured Cards")
            print("=" * 55)
            print(
                "The following cards were not found in database.py"
            )
            print("and will be treated as generic 'OTHER' cards during simulation:")
            for card_name in self.other_cards:
                print(f"  • {card_name}")
            print("=" * 55 + "\n")
        else:
            print(
                "\n✅ All loaded decklist cards were recognized in database.py!\n"
            )

    def get_cards(self) -> list:
        """Returns the list of 99 Card objects."""
        return self.cards

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"<Deck: {len(self.cards)} cards loaded>"
