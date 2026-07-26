import random
from src.card import Card
from src.database import get_card
from src.deck import Deck

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
    """Motor de simulación paso a paso para evaluar el combo de Zirda en Turno 2."""

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

        for mulligan_cnt in range(3):
            self.log = []
            hand = self.apply_london_mulligan(list(opening_7), mulligan_cnt)
            board = []
            library = list(deck_cards)

            self.trace(f"\n--- INICIO DE PARTIDA (Mulligans: {mulligan_cnt}) ---")
            self.trace(f"Mano Inicial: {[c.name for c in hand]}")

            # --- FASE PREGAME ---
            gemstone = next(
                (c for c in hand if c.name == "Gemstone Caverns"), None
            )
            if gemstone and random.random() < 0.75:
                other = next(
                    (
                        c
                        for c in hand
                        if c.role == "Other" or c.name == "OTHER"
                    ),
                    None,
                )
                if other:
                    hand.remove(other)
                    hand.remove(gemstone)
                    board.append(gemstone)
                    self.trace(
                        f"Pregame: Play Gemstone Caverns (Exilada {other.name})"
                    )

            # --- TURNO 1 (T1) ---
            lands_t1 = [c for c in hand if c.role == "Land"]
            if lands_t1:
                chosen_land = lands_t1[0]
                for l in lands_t1:
                    if l.name in [
                        "COLOR_LAND",
                        "Mishra's Workshop",
                        "Ancient Tomb",
                    ]:
                        chosen_land = l
                        break
                hand.remove(chosen_land)
                board.append(chosen_land)
                self.trace(f"T1 Land Drop: Play {chosen_land.name}")

            # Acciones / Casts de T1
            gamble = next((c for c in hand if c.name == "Gamble"), None)
            if gamble:
                has_red_t1 = any(
                    c.name in ["COLOR_LAND", "Gemstone Caverns"] for c in board
                )
                if has_red_t1:
                    hand.remove(gamble)
                    grim = get_card("Grim Monolith")
                    hand.append(grim)

                    discarded = random.choice(hand)
                    hand.remove(discarded)
                    self.trace(
                        f"T1 Action: Cast Gamble ({gamble.cost_pips}) -> Busca Grim Monolith y descarta al azar: {discarded.name}"
                    )

            # --- TURNO 2 (T2) ---
            if library:
                drawn = library.pop()
                hand.append(drawn)
                self.trace(f"T2 Draw Step: Robada {drawn.name}")

            lands_t2 = [c for c in hand if c.role == "Land"]
            if lands_t2:
                chosen_t2 = lands_t2[0]
                board.append(chosen_t2)
                hand.remove(chosen_t2)
                self.trace(f"T2 Land Drop: Play {chosen_t2.name}")

            self.trace(f"Mano al inicio de T2: {[c.name for c in hand]}")

            # --- SECUENCIADOR Y CASTS DE T2 ---
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

            # 1. Ephemeral & Fast Mana
            petal = next((c for c in hand if c.name == "Lotus Petal"), None)
            if petal:
                hand.remove(petal)
                pool_r += 1
                self.trace("T2 Action: Cast Lotus Petal (Coste: {0}) -> Sacrifica (+1 Mana Color)")

            ssg = next((c for c in hand if c.name == "Simian Spirit Guide"), None)
            if ssg:
                hand.remove(ssg)
                pool_r += 1
                self.trace("T2 Action: Exile Simian Spirit Guide de la mano (+1 Rojo)")

            # 2. Casts de Rituales
            seething = next((c for c in hand if c.name == "Seething Song"), None)
            if seething and pool_r >= 1 and (pool_r + pool_c) >= 3:
                hand.remove(seething)
                if pool_c >= 2:
                    pool_c -= 2
                    pool_r -= 1
                else:
                    rem = 2 - pool_c
                    pool_c = 0
                    pool_r -= 1 + rem
                pool_r += 5
                self.trace("T2 Action: Cast Seething Song (Coste: {2}{R}) -> Genera +5{R}")

            pyretic = next(
                (
                    c
                    for c in hand
                    if c.name in ["Pyretic Ritual", "Desperate Ritual"]
                ),
                None,
            )
            if pyretic and pool_r >= 1 and (pool_r + pool_c) >= 2:
                hand.remove(pyretic)
                if pool_c >= 1:
                    pool_c -= 1
                    pool_r -= 1
                else:
                    pool_r -= 2
                pool_r += 3
                self.trace(f"T2 Action: Cast {pyretic.name} (Coste: {{1}}{{R}}) -> Genera +3{{R}}")

            # 3. Casts de Monolito
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
                    self.trace(
                        "T2 Action: Cast Grim Monolith (Coste: {2}) -> Tapea para +3{C}"
                    )
                elif basalt and (pool_r + pool_c) >= 3:
                    hand.remove(basalt)
                    board.append(basalt)
                    pool_c += 3
                    monolith_in_play = True
                    self.trace(
                        "T2 Action: Cast Basalt Monolith (Coste: {3}) -> Tapea para +3{C}"
                    )

            # 4. Cast de Comandante (Zirda)
            zirda_ready = False
            if monolith_in_play and pool_r >= 2 and (pool_r + pool_c) >= 3:
                zirda_ready = True
                self.trace("T2 Action: Cast Zirda, the Dawnwaker desde la Command Zone (Coste: {1}{R/W}{R/W})")

            # 5. Cast de Rematador (Outlet)
            outlet_card = next((c for c in hand if c.role == "Outlet"), None)

            if zirda_ready and monolith_in_play and outlet_card:
                self.trace(f"T2 Action: Cast {outlet_card.name} (Outlet) -> Ejecuta maná infinito con Monolito")
                self.trace(f"Board State Final: {[c.name for c in board]}")
                self.trace(f"Mano Restante: {[c.name for c in hand]}")
                self.trace("🏆 RESULTADO: VICTORIA EN TURNO 2")
                return True, f"T2 Win (Mulligan {mulligan_cnt})"

            # Registro en caso de fallo
            self.trace(f"Board State Final: {[c.name for c in board]}")
            self.trace(f"Mano Restante: {[c.name for c in hand]}")
            self.trace("❌ RESULTADO: FALLO EN TURNO 2")

        return False, "T2 Fail"
