import random
from src.card import Card
from src.database import get_card
from src.deck import Deck

# Mulligan discard priority (cards at the top of this list are discarded first)
DISCARD_PRIORITY = [
    "OTHER",
    "Aurelia's Fury",
    "Apple of Eden, Isu Relic",
    "Staff of Compleation",
    "Staff of Domination",
    "Cogwork Assembler",
    "Walking Ballista",
    "Seething Song",
    "Jeska's Will",
    "Desperate Ritual",
    "Pyretic Ritual",
    "Rite of Flame",
    "COLOR_LAND",
    "Urza's Saga",
    "City of Traitors",
    "Ancient Tomb",
    "Mishra's Workshop",
    "Gemstone Caverns",
    "Arcane Signet",
    "Talisman of Conviction",
    "Simian Spirit Guide",
    "Lotus Petal",
    "Mox Opal",
    "Mox Diamond",
    "Chrome Mox",
    "Tezzeret, Cruel Captain",
    "Reckless Handling",
    "Moonsilver Key",
    "Gamble",
    "Enlightened Tutor",
    "Mana Vault",
    "Sol Ring",
    "Grim Monolith",
    "Basalt Monolith",
]


class GameEngine:
    """Simulates a game state to test Turn 1 - Turn 3 combo execution."""

    def __init__(self, deck: Deck, debug: bool = False):
        self.raw_deck = list(deck.get_cards())
        self.debug = debug
        self.log = []

    def trace(self, msg: str):
        if self.debug:
            self.log.append(msg)

    def apply_london_mulligan(
        self, hand: list[Card], num_discards: int
    ) -> list[Card]:
        if num_discards == 0:
            return hand

        def get_priority(card: Card) -> int:
            if card.name in DISCARD_PRIORITY:
                return DISCARD_PRIORITY.index(card.name)
            return 0

        sorted_hand = sorted(hand, key=get_priority)
        return sorted_hand[num_discards:]

    def run_simulation(self) -> tuple[bool, str]:
        deck_cards = list(self.raw_deck)
        random.shuffle(deck_cards)

        opening_7 = [deck_cards.pop() for _ in range(7)]

        for mulligan_cnt in range(3):  # Max 2 mulligans (7, 6, 5)
            self.log = []
            hand = self.apply_london_mulligan(list(opening_7), mulligan_cnt)
            board = []
            library = list(deck_cards)

            self.trace(f"\n--- STARTING HAND (Mulligans: {mulligan_cnt}) ---")
            self.trace(f"Hand: {[c.name for c in hand]}")

            # --- PREGAME PHASE (Gemstone Caverns) ---
            gemstone = next(
                (c for c in hand if c.name == "Gemstone Caverns"), None
            )
            if gemstone and random.random() < 0.75:  # Assume off-play 75%
                other = next((c for c in hand if c.role == "Other"), None)
                if other:
                    hand.remove(other)
                    hand.remove(gemstone)
                    board.append(gemstone)
                    self.trace(
                        "Pregame: Gemstone Caverns active (exiled 1 card)"
                    )

            # --- TURN 1 PHASE ---
            # Land Drop
            lands = [c for c in hand if c.role == "Land"]
            if lands:
                # Prefer color land or Workshop
                chosen_land = lands[0]
                for l in lands:
                    if l.name in [
                        "COLOR_LAND",
                        "Mishra's Workshop",
                        "Ancient Tomb",
                    ]:
                        chosen_land = l
                        break
                hand.remove(chosen_land)
                board.append(chosen_land)
                self.trace(f"T1 Land Drop: {chosen_land.name}")

            # --- TURN 2 PHASE ---
            # Draw Step
            if library:
                drawn = library.pop()
                hand.append(drawn)
                self.trace(f"T2 Draw Step: Drew {drawn.name}")

            # T2 Land Drop
            lands_t2 = [c for c in hand if c.role == "Land"]
            if lands_t2:
                board.append(lands_t2[0])
                hand.remove(lands_t2[0])
                self.trace(f"T2 Land Drop: {lands_t2[0].name}")

            # --- T2 MANA POOL & EXECUTION SEQUENCER ---
            pool_r = sum(
                1
                for c in board
                if c.name
                in [
                    "COLOR_LAND",
                    "Gemstone Caverns",
                    "Arcane Signet",
                    "Talisman of Conviction",
                    "Chrome Mox",
                    "Mox Diamond",
                    "Mox Opal",
                ]
            )
            pool_c = sum(
                3
                if c.name in ["Sol Ring", "Mana Vault", "Grim Monolith"]
                else 2
                if c.name in ["Ancient Tomb", "City of Traitors"]
                else 1
                for c in board
                if c.name != "Mishra's Workshop"
            )

            # 1. Ephemeral & Ritual Mana
            petal = next((c for c in hand if c.name == "Lotus Petal"), None)
            if petal:
                hand.remove(petal)
                pool_r += 1
                self.trace("T2 Action: Played Lotus Petal (+1 Red/White)")

            ssg = next((c for c in hand if c.name == "Simian Spirit Guide"), None)
            if ssg:
                hand.remove(ssg)
                pool_r += 1
                self.trace("T2 Action: Exiled Simian Spirit Guide (+1 Red)")

            # Ritual execution checks
            seething = next((c for c in hand if c.name == "Seething Song"), None)
            if seething and pool_r >= 1 and (pool_r + pool_c) >= 3:
                hand.remove(seething)
                # Pay 2 generic + 1 Red
                if pool_c >= 2:
                    pool_c -= 2
                    pool_r -= 1
                else:
                    rem = 2 - pool_c
                    pool_c = 0
                    pool_r -= 1 + rem
                pool_r += 5
                self.trace("T2 Action: Cast Seething Song (+5 Red)")

            # 2. Check Monolith Piece
            monolith_in_play = any(
                c.name in ["Basalt Monolith", "Grim Monolith"] for c in board
            )

            if not monolith_in_play:
                basalt = next(
                    (c for c in hand if c.name == "Basalt Monolith"), None
                )
                grim = next((c for c in hand if c.name == "Grim Monolith"), None)

                if grim and (pool_r + pool_c) >= 2:
                    hand.remove(grim)
                    board.append(grim)
                    pool_c += 3
                    monolith_in_play = True
                    self.trace("T2 Action: Cast & Tapped Grim Monolith")
                elif basalt and (pool_r + pool_c) >= 3:
                    hand.remove(basalt)
                    board.append(basalt)
                    pool_c += 3
                    monolith_in_play = True
                    self.trace("T2 Action: Cast & Tapped Basalt Monolith")

            # 3. Check Zirda Castability (Requires 2 Color Pips + 1 Generic)
            zirda_ready = False
            if monolith_in_play and pool_r >= 2 and (pool_r + pool_c) >= 3:
                zirda_ready = True
                self.trace("T2 Action: Cast Zirda, the Dawnwaker")

            # 4. Check Outlet
            has_outlet = any(c.role == "Outlet" for c in hand)

            if zirda_ready and monolith_in_play and has_outlet:
                self.trace("🏆 RESULT: TURN 2 VICTORY VALIDATED STEP-BY-STEP")
                return True, f"T2 Win (Mulligan {mulligan_cnt})"

        return False, "T2 Fail"
