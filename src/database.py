from src.card import Card

# Master card database defining attributes for cards in the combo ecosystem
CARD_DATABASE = {
    # --- TIERRAS (LANDS) ---
    "COLOR_LAND": Card(
        name="COLOR_LAND",
        card_type="Land",
        role="Land",
        mana_produced={"R": 1, "W": 1, "C": 0},
    ),
    "Ancient Tomb": Card(
        name="Ancient Tomb",
        card_type="Land",
        role="Land",
        mana_produced={"R": 0, "W": 0, "C": 2},
    ),
    "City of Traitors": Card(
        name="City of Traitors",
        card_type="Land",
        role="Land",
        mana_produced={"R": 0, "W": 0, "C": 2},
    ),
    "Mishra's Workshop": Card(
        name="Mishra's Workshop",
        card_type="Land",
        role="Land",
        mana_produced={"R": 0, "W": 0, "C": 3},
        restrictions=["only_artifacts"],
    ),
    "Gemstone Caverns": Card(
        name="Gemstone Caverns",
        card_type="Land",
        role="Land",
        mana_produced={"R": 1, "W": 1, "C": 0},
        restrictions=["pregame_exile_option"],
    ),
    "Urza's Saga": Card(
        name="Urza's Saga",
        card_type="Land",
        role="Land",
        mana_produced={"R": 0, "W": 0, "C": 1},
        restrictions=["t3_tutor"],
    ),
    # --- MANA ROCKS ---
    "Sol Ring": Card(
        name="Sol Ring",
        card_type="Artifact",
        role="Mana_Rock",
        cost_generic=1,
        mana_produced={"R": 0, "W": 0, "C": 2},
    ),
  "Talisman of Conviction": Card(
        name="Talisman of Conviction",
        card_type="Artifact",
        role="Mana_Rock",
        cost_generic=2,
        mana_produced={"R": 1, "W": 1, "C": 0},
  ),
    "Mana Vault": Card(
        name="Mana Vault",
        card_type="Artifact",
        role="Mana_Rock",
        cost_generic=1,
        mana_produced={"R": 0, "W": 0, "C": 3},
    ),
    "Arcane Signet": Card(
        name="Arcane Signet",
        card_type="Artifact",
        role="Mana_Rock",
        cost_generic=2,
        mana_produced={"R": 1, "W": 1, "C": 0},
    ),
    "Chrome Mox": Card(
        name="Chrome Mox",
        card_type="Artifact",
        role="Mana_Rock",
        cost_generic=0,
        mana_produced={"R": 1, "W": 1, "C": 0},
        restrictions=["imprint_non_artifact"],
    ),
    "Mox Diamond": Card(
        name="Mox Diamond",
        card_type="Artifact",
        role="Mana_Rock",
        cost_generic=0,
        mana_produced={"R": 1, "W": 1, "C": 0},
        restrictions=["discard_land_cost"],
    ),
    "Mox Opal": Card(
        name="Mox Opal",
        card_type="Artifact",
        role="Mana_Rock",
        cost_generic=0,
        mana_produced={"R": 1, "W": 1, "C": 0},
        restrictions=["requires_metalcraft"],
    ),
    # --- RITUALS & EPHEMERAL MANA ---
    "Lotus Petal": Card(
        name="Lotus Petal",
        card_type="Artifact",
        role="Ritual",
        cost_generic=0,
        mana_produced={"R": 1, "W": 1, "C": 0},
        is_ephemeral=True,
    ),
    "Simian Spirit Guide": Card(
        name="Simian Spirit Guide",
        card_type="Creature",
        role="Ritual",
        cost_generic=0,
        mana_produced={"R": 1, "W": 0, "C": 0},
        is_ephemeral=True,
    ),
    "Rite of Flame": Card(
        name="Rite of Flame",
        card_type="Sorcery",
        role="Ritual",
        cost_generic=0,
        cost_pips={"R": 1, "W": 0},
        mana_produced={"R": 2, "W": 0, "C": 0},
        is_ephemeral=True,
    ),
    "Pyretic Ritual": Card(
        name="Pyretic Ritual",
        card_type="Instant",
        role="Ritual",
        cost_generic=1,
        cost_pips={"R": 1, "W": 0},
        mana_produced={"R": 3, "W": 0, "C": 0},
        is_ephemeral=True,
    ),
    "Desperate Ritual": Card(
        name="Desperate Ritual",
        card_type="Instant",
        role="Ritual",
        cost_generic=1,
        cost_pips={"R": 1, "W": 0},
        mana_produced={"R": 3, "W": 0, "C": 0},
        is_ephemeral=True,
    ),
    "Seething Song": Card(
        name="Seething Song",
        card_type="Instant",
        role="Ritual",
        cost_generic=2,
        cost_pips={"R": 1, "W": 0},
        mana_produced={"R": 5, "W": 0, "C": 0},
        is_ephemeral=True,
    ),
    "Jeska's Will": Card(
        name="Jeska's Will",
        card_type="Sorcery",
        role="Ritual",
        cost_generic=2,
        cost_pips={"R": 1, "W": 0},
        mana_produced={"R": 5, "W": 0, "C": 0},
        is_ephemeral=True,
    ),
    # --- TUTORS ---
    "Gamble": Card(
        name="Gamble",
        card_type="Sorcery",
        role="Tutor",
        cost_generic=0,
        cost_pips={"R": 1, "W": 0},
        restrictions=["random_discard"],
    ),
    "Enlightened Tutor": Card(
        name="Enlightened Tutor",
        card_type="Instant",
        role="Tutor",
        cost_generic=0,
        cost_pips={"R": 0, "W": 1},
        restrictions=["put_on_top"],
    ),
    "Moonsilver Key": Card(
        name="Moonsilver Key",
        card_type="Artifact",
        role="Tutor",
        cost_generic=3,
        restrictions=["fetch_mana_artifact"],
    ),
 "Reckless Handling": Card(
        name="Gamble",
        card_type="Sorcery",
        role="Tutor",
        cost_generic=1,
        cost_pips={"R": 1, "W": 0},
        restrictions=["random_discard"],
    ),
  
    # --- COMBO PIECES ---
    "Basalt Monolith": Card(
        name="Basalt Monolith",
        card_type="Artifact",
        role="Piece",
        cost_generic=3,
        mana_produced={"R": 0, "W": 0, "C": 3},
    ),
    "Grim Monolith": Card(
        name="Grim Monolith",
        card_type="Artifact",
        role="Piece",
        cost_generic=2,
        mana_produced={"R": 0, "W": 0, "C": 3},
    ),
    # --- OUTLETS ---
    "Walking Ballista": Card(
        name="Walking Ballista",
        card_type="Artifact",
        role="Outlet",
        cost_generic=0,
    ),
    "Cogwork Assembler": Card(
        name="Cogwork Assembler",
        card_type="Artifact",
        role="Outlet",
        cost_generic=3,
    ),
    "Staff of Domination": Card(
        name="Staff of Domination",
        card_type="Artifact",
        role="Outlet",
        cost_generic=3,
    ),
    "Staff of Compleation": Card(
        name="Staff of Compleation",
        card_type="Artifact",
        role="Outlet",
        cost_generic=3,
    ),
    "Tezzeret, Cruel Captain": Card(
        name="Tezzeret, Cruel Captain",
        card_type="Creature",
        role="Outlet",
        cost_generic=3,
    ),
    "Aurelia's Fury": Card(
        name="Aurelia's Fury",
        card_type="Instant",
        role="Outlet",
        cost_generic=0,
        cost_pips={"R": 1, "W": 1},
    ),
  "Apple of Eden, Isu Relic": Card(
        name="Apple of Eden, Isu Relic",
        card_type="Artifact",
        role="Outlet",
        cost_generic=4,
    ),
}


def get_card(name: str) -> Card:
    """Returns a Card object from database or a generic filler card if not explicitly configured."""
    if name in CARD_DATABASE:
        return CARD_DATABASE[name]
    return Card(name=name, card_type="Unknown", role="Other")
