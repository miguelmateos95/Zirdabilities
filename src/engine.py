# ==============================================================================
# MOTOR DE JUEGO, LÓGICA DE DECISIÓN Y LONDON MULLIGAN (ZIRDA SIMULATOR)
# ==============================================================================

import random


class GameState:

    def __init__(self, hand, deck_cards):
        self.hand = list(hand)
        self.library = list(deck_cards)
        self.battlefield = []
        self.graveyard = []
        self.mana_pool = {"C": 0, "R": 0, "W": 0, "generic": 0}
        self.lands_played_this_turn = 0
        self.zirda_in_command_zone = True
        self.zirda_on_battlefield = False

    def reset_mana(self):
        self.mana_pool = {"C": 0, "R": 0, "W": 0, "generic": 0}

    def total_mana(self):
        return sum(self.mana_pool.values())

    @property
    def artifacts_count(self):
        return sum(
            1
            for card in self.battlefield
            if getattr(card, "is_artifact", False)
            or getattr(card, "type", "") == "artifact"
        )


class GameEngine:

    def __init__(self, deck, max_mulligans=2, debug=False, *args, **kwargs):
        self.deck = deck
        self.max_mulligans = max_mulligans
        self.debug = debug
        self.mulligans = 0
        self.state = None
        self._setup_hand_with_london_mulligan(self.max_mulligans)

    def _is_keepable_hand(self, hand):
        """Criterio cEDH para evaluar si se conserva la mano."""
        lands = [
            c
            for c in hand
            if getattr(c, "role", "") == "LAND"
            or getattr(c, "type", "") == "land"
        ]
        fast_mana = [
            c
            for c in hand
            if getattr(c, "role", "") in ["FAST_MANA", "MANA_ROCK", "RITUAL"]
        ]
        monoliths = [c for c in hand if getattr(c, "is_monolith", False)]
        tutors_or_outlets = [
            c
            for c in hand
            if getattr(c, "is_outlet", False)
            or getattr(c, "tutor_artifact", False)
            or getattr(c, "name", "")
            in ["Enlightened Tutor", "Gamble", "Imperial Recruiter"]
        ]

        # 1. Al menos 1 fuente de maná
        if len(lands) + len(fast_mana) < 1:
            return False

        # 2. Presencia de pieza de combo o aceleración fuerte
        if monoliths:
            return True
        if len(fast_mana) >= 2 and tutors_or_outlets:
            return True
        if len(lands) >= 2 and (fast_mana or tutors_or_outlets):
            return True

        return False

    def _setup_hand_with_london_mulligan(self, max_mulligans):
        """Aplica las reglas del London Mulligan oficial de Magic."""
        cards = self.deck.get_cards()

        for mull_count in range(max_mulligans + 1):
            random.shuffle(cards)
            drawn_hand = cards[:7]
            remaining_library = cards[7:]

            if self._is_keepable_hand(drawn_hand) or mull_count == max_mulligans:
                self.mulligans = mull_count

                if mull_count > 0:
                    # Retener piezas claves, descartar 'OTHER'
                    drawn_hand.sort(
                        key=lambda c: 0
                        if getattr(c, "is_monolith", False)
                        or getattr(c, "is_outlet", False)
                        else (
                            1
                            if getattr(c, "role", "") in ["LAND", "FAST_MANA"]
                            else 2
                        )
                    )
                    bottom_cards = drawn_hand[-mull_count:]
                    final_hand = drawn_hand[:-mull_count]
                    remaining_library.extend(bottom_cards)
                else:
                    final_hand = drawn_hand

                self.state = GameState(final_hand, remaining_library)
                break

    def draw_card(self):
        if self.state.library:
            card = self.state.library.pop(0)
            self.state.hand.append(card)

    def execute_turn(self, turn_number):
        self.state.lands_played_this_turn = 0
        self.state.reset_mana()

        # Robo de carta en T2+
        if turn_number > 1:
            self.draw_card()

        # Secuencia del turno
        self._tap_board_for_mana()
        self._play_land()
        self._play_fast_mana_and_rituals()
        self._play_combo_pieces()

    def _tap_board_for_mana(self):
        for card in self.state.battlefield:
            if getattr(card, "type", "") == "land":
                produces = getattr(card, "produces", ["C"])
                if "R" in produces:
                    self.state.mana_pool["R"] += 1
                elif "W" in produces:
                    self.state.mana_pool["W"] += 1
                else:
                    self.state.mana_pool["C"] += 1

            elif getattr(card, "role", "") in ["FAST_MANA", "MANA_ROCK"]:
                mana_added = getattr(card, "mana_added", {})
                for k, v in mana_added.items():
                    if k in self.state.mana_pool:
                        self.state.mana_pool[k] += v
                    else:
                        self.state.mana_pool["C"] += v

    def _play_land(self):
        if self.state.lands_played_this_turn >= 1:
            return

        lands_in_hand = [
            c
            for c in self.state.hand
            if getattr(c, "role", "") == "LAND"
            or getattr(c, "type", "") == "land"
        ]
        if not lands_in_hand:
            return

        selected_land = lands_in_hand[0]
        for land in lands_in_hand:
            if any(
                color in getattr(land, "produces", []) for color in ["R", "W"]
            ):
                selected_land = land
                break

        self.state.hand.remove(selected_land)
        self.state.battlefield.append(selected_land)
        self.state.lands_played_this_turn += 1

        produces = getattr(selected_land, "produces", ["C"])
        if "R" in produces:
            self.state.mana_pool["R"] += 1
        elif "W" in produces:
            self.state.mana_pool["W"] += 1
        else:
            self.state.mana_pool["C"] += 1

    def _play_fast_mana_and_rituals(self):
        playable = True
        while playable:
            playable = False
            for card in list(self.state.hand):
                if getattr(card, "role", "") == "FAST_MANA":
                    cost = 1 if getattr(card, "cost", "0") == "1" else 0
                    if self.state.total_mana() >= cost:
                        self.state.hand.remove(card)
                        self.state.battlefield.append(card)
                        added = getattr(card, "mana_added", {"C": 2})
                        for k, v in added.items():
                            if k in self.state.mana_pool:
                                self.state.mana_pool[k] += v
                            else:
                                self.state.mana_pool["C"] += v
                        playable = True

                elif getattr(card, "role", "") == "RITUAL":
                    name = getattr(card, "name", "")
                    if name == "Rite of Flame" and self.state.mana_pool["R"] >= 1:
                        self.state.mana_pool["R"] += 1
                        self.state.hand.remove(card)
                        self.state.graveyard.append(card)
                        playable = True
                    elif (
                        name == "_____ Goblin"
                        and self.state.total_mana() >= 3
                        and self.state.mana_pool["R"] >= 1
                    ):
                        self.state.mana_pool["R"] += 3
                        self.state.hand.remove(card)
                        self.state.graveyard.append(card)
                        playable = True

    def _play_combo_pieces(self):
        # 1. Monolito
        monoliths = [
            c for c in self.state.hand if getattr(c, "is_monolith", False)
        ]
        for mon in monoliths:
            cost = 3 if getattr(mon, "name", "") == "Basalt Monolith" else 2
            if self.state.total_mana() >= cost:
                self.state.hand.remove(mon)
                self.state.battlefield.append(mon)
                break

        # 2. Zirda desde la Zona de Comandante (1RW)
        has_monolith = any(
            getattr(c, "is_monolith", False) for c in self.state.battlefield
        )
        if has_monolith and self.state.zirda_in_command_zone:
            if self.state.total_mana() >= 3 and (
                self.state.mana_pool["R"] >= 1 or self.state.mana_pool["W"] >= 1
            ):
                self.state.zirda_in_command_zone = False
                self.state.zirda_on_battlefield = True

        # 3. Outlet
        outlets = [c for c in self.state.hand if getattr(c, "is_outlet", False)]
        for out in outlets:
            if self.state.total_mana() >= 1:
                self.state.hand.remove(out)
                self.state.battlefield.append(out)
                break

    def check_win(self):
        """Condición de victoria del combo infinito."""
        has_monolith = any(
            getattr(c, "is_monolith", False) for c in self.state.battlefield
        )
        has_outlet = any(
            getattr(c, "is_outlet", False) for c in self.state.battlefield
        )
        return has_monolith and self.state.zirda_on_battlefield and has_outlet

    def run_simulation(self, max_turns=2):
        """Retorna tupla (éxito: bool, razón: str) esperada por main.py"""
        for turn in range(1, max_turns + 1):
            self.execute_turn(turn)
            if self.check_win():
                return True, f"Combo completado en Turno {turn}"
        return False, "No se completó el combo en Turno 2"


# Aliases por compatibilidad
Game = GameEngine
Engine = GameEngine
