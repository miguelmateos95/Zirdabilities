# ==============================================================================
# BASE DE DATOS COMPLETA DE CARTAS (ZIRDA SIMULATION)
# ==============================================================================

CARDS_DATABASE = {
    # --------------------------------------------------------------------------
    # 1. PIEZAS CORE DEL COMBO Y BASE PREVIA
    # --------------------------------------------------------------------------
    "Basalt Monolith": {
        "cost": "3",
        "type": "artifact",
        "role": "MONOLITH",
        "is_monolith": True,
        "mana_produced": 3,
        "untap_cost": 3,
    },
    "Grim Monolith": {
        "cost": "2",
        "type": "artifact",
        "role": "MONOLITH",
        "is_monolith": True,
        "mana_produced": 3,
        "untap_cost": 4,
    },
    "Monolith": {
        "cost": "3",
        "type": "artifact",
        "role": "MONOLITH",
        "is_monolith": True,
    },
    # Outlets / Condición de Victoria
    "Walking Ballista": {
        "cost": "XX",
        "type": "artifact_creature",
        "role": "OUTLET",
        "is_outlet": True,
    },
    "Staff of Domination": {
        "cost": "3",
        "type": "artifact",
        "role": "OUTLET",
        "is_outlet": True,
        "activated_ability_cost": "1",
    },
    "Diviner's Wand": {
        "cost": "3",
        "type": "artifact",
        "role": "OUTLET",
        "is_outlet": True,
        "activated_ability_cost": "4",
    },
    "Sanctum of Eternity": {
        "type": "land",
        "role": "OUTLET",
        "produces": ["C"],
        "is_outlet": True,
    },
    # Fast Mana Base Previos
    "Sol Ring": {
        "cost": "1",
        "type": "artifact",
        "role": "FAST_MANA",
        "mana_added": {"C": 2},
    },
    "Mana Crypt": {
        "cost": "0",
        "type": "artifact",
        "role": "FAST_MANA",
        "mana_added": {"C": 2},
    },
    "Mana Vault": {
        "cost": "1",
        "type": "artifact",
        "role": "FAST_MANA",
        "mana_added": {"C": 3},
    },
    "Mox Diamond": {
        "cost": "0",
        "type": "artifact",
        "role": "FAST_MANA",
        "mana_added": {"any": 1},
    },
    "Chrome Mox": {
        "cost": "0",
        "type": "artifact",
        "role": "FAST_MANA",
        "mana_added": {"any": 1},
    },
    "Lotus Petal": {
        "cost": "0",
        "type": "artifact",
        "role": "FAST_MANA",
        "mana_added": {"any": 1},
    },
    "Arcane Signet": {
        "cost": "2",
        "type": "artifact",
        "role": "MANA_ROCK",
        "mana_added": {"R": 1, "W": 1},
    },
    "Boros Signet": {
        "cost": "2",
        "type": "artifact",
        "role": "MANA_ROCK",
        "mana_added": {"R": 1, "W": 1},
    },
    "Talisman of Conviction": {
        "cost": "2",
        "type": "artifact",
        "role": "MANA_ROCK",
        "mana_added": {"R": 1, "W": 1},
    },
    # --------------------------------------------------------------------------
    # 2. TIERRAS
    # --------------------------------------------------------------------------
    "Arid Mesa": {
        "type": "land",
        "role": "LAND",
        "produces": ["R", "W"],
        "is_fetch": True,
    },
    "Bloodstained Mire": {
        "type": "land",
        "role": "LAND",
        "produces": ["R", "W"],
        "is_fetch": True,
    },
    "Marsh Flats": {
        "type": "land",
        "role": "LAND",
        "produces": ["R", "W"],
        "is_fetch": True,
    },
    "Wooded Foothills": {
        "type": "land",
        "role": "LAND",
        "produces": ["R", "W"],
        "is_fetch": True,
    },
    "Battlefield Forge": {
        "type": "land",
        "role": "LAND",
        "produces": ["C", "R", "W"],
    },
    "City of Brass": {"type": "land", "role": "LAND", "produces": ["R", "W"]},
    "Command Tower": {"type": "land", "role": "LAND", "produces": ["R", "W"]},
    "Exotic Orchard": {"type": "land", "role": "LAND", "produces": ["R", "W"]},
    "Great Furnace": {
        "type": "land",
        "role": "LAND",
        "produces": ["R"],
        "is_artifact": True,
    },
    "Mana Confluence": {"type": "land", "role": "LAND", "produces": ["R", "W"]},
    "Mountain": {"type": "land", "role": "LAND", "produces": ["R"]},
    "Plains": {"type": "land", "role": "LAND", "produces": ["W"]},
    "Plateau": {"type": "land", "role": "LAND", "produces": ["R", "W"]},
    "Sacred Foundry": {"type": "land", "role": "LAND", "produces": ["R", "W"]},
    "Spectator Seating": {"type": "land", "role": "LAND", "produces": ["R", "W"]},
    "Starting Town": {"type": "land", "role": "LAND", "produces": ["R", "W"]},
    "Sunbaked Canyon": {"type": "land", "role": "LAND", "produces": ["R", "W"]},
    "Emergence Zone": {"type": "land", "role": "LAND", "produces": ["C"]},
    "Treasure Vault": {
        "type": "land",
        "role": "LAND",
        "produces": ["C"],
        "is_artifact": True,
    },
    "Abstergo Entertainment": {
        "type": "land",
        "role": "LAND",
        "produces": ["C"],
        "filter_ability": True,
    },
    "Spire of Industry": {
        "type": "land",
        "role": "LAND",
        "produces_conditional": lambda state: (
            ["R", "W"] if getattr(state, "artifacts_count", 0) > 0 else ["C"]
        ),
    },
    "Inventors' Fair": {
        "type": "land",
        "role": "LAND",
        "produces": ["C"],
        "can_tutor_artifact": lambda state: getattr(state, "artifacts_count", 0)
        >= 3,
    },
    # --------------------------------------------------------------------------
    # 3. MANA FAST / RITUALES / OUTLETS NUEVOS
    # --------------------------------------------------------------------------
    "_____ Goblin": {
        "cost": "2R",
        "type": "ritual",
        "role": "RITUAL",
        "mana_added": {"R": 5},
    },
    "Treasonous Ogre": {
        "cost": "3R",
        "type": "creature",
        "role": "RITUAL",
        "pay_life_for_mana": {"R": 10},
    },
    "Lion's Eye Diamond": {
        "cost": "0",
        "type": "artifact",
        "role": "FAST_MANA",
        "is_led": True,
    },
    "Kozilek's Command": {
        "cost": "XCC",
        "type": "instant",
        "role": "OUTLET",
        "is_outlet": True,
    },
    "Thran Spider": {
        "cost": "3",
        "type": "artifact_creature",
        "role": "OUTLET",
        "is_outlet": True,
        "activated_ability_cost": "7",
    },
    # --------------------------------------------------------------------------
    # 4. UTILITY Y OTROS (ROLE = OTHER / UTILITY)
    # --------------------------------------------------------------------------
    "Rings of Brighthearth": {"cost": "3", "type": "artifact", "role": "UTILITY"},
    "Manifold Key": {"cost": "1", "type": "artifact", "role": "UTILITY"},
    "Voltaic Key": {"cost": "1", "type": "artifact", "role": "UTILITY"},
    "Mirage Mirror": {"cost": "3", "type": "artifact", "role": "UTILITY"},
    "Scroll Rack": {"cost": "2", "type": "artifact", "role": "UTILITY"},
    "The One Ring": {"cost": "4", "type": "artifact", "role": "UTILITY"},
    "Goblin Engineer": {"cost": "1R", "type": "creature", "role": "UTILITY"},
    "Oswald Fiddlebender": {"cost": "1W", "type": "creature", "role": "UTILITY"},
    "Archivist of Oghma": {"cost": "1W", "type": "other", "role": "OTHER"},
    "Black Widow, Agile Avenger": {"cost": "1R", "type": "other", "role": "OTHER"},
    "Borrowed Knowledge": {"cost": "1W", "type": "other", "role": "OTHER"},
    "Deflecting Swat": {"cost": "0", "type": "instant", "role": "OTHER"},
    "Delivery Moogle": {"cost": "2W", "type": "other", "role": "OTHER"},
    "Drannith Magistrate": {"cost": "1W", "type": "other", "role": "OTHER"},
    "Esper Sentinel": {"cost": "W", "type": "other", "role": "OTHER"},
    "Ethersworn Canonist": {"cost": "1W", "type": "other", "role": "OTHER"},
    "Final Fortune": {"cost": "RR", "type": "instant", "role": "OTHER"},
    "Hex Magic": {"cost": "1R", "type": "other", "role": "OTHER"},
    "Jolted Awake": {"cost": "W", "type": "other", "role": "OTHER"},
    "Liberator, Urza's Battlethopter": {
        "cost": "3",
        "type": "other",
        "role": "OTHER",
    },
    "Orim's Chant": {"cost": "W", "type": "instant", "role": "OTHER"},
    "Portable Hole": {"cost": "W", "type": "other", "role": "OTHER"},
    "Pyroblast": {"cost": "R", "type": "instant", "role": "OTHER"},
    "Ragavan, Nimble Pilferer": {"cost": "R", "type": "creature", "role": "OTHER"},
    "Recommission": {"cost": "1W", "type": "other", "role": "OTHER"},
    "Red Elemental Blast": {"cost": "R", "type": "instant", "role": "OTHER"},
    "Redirect Lightning": {"cost": "1R", "type": "instant", "role": "OTHER"},
    "Sevinne's Reclamation": {"cost": "2W", "type": "other", "role": "OTHER"},
    "Silence": {"cost": "W", "type": "instant", "role": "OTHER"},
    "Smothering Tithe": {"cost": "3W", "type": "enchantment", "role": "OTHER"},
    "Swords to Plowshares": {"cost": "W", "type": "instant", "role": "OTHER"},
    "Tataru Taru": {"cost": "1W", "type": "other", "role": "OTHER"},
    "Touch the Spirit Realm": {"cost": "2W", "type": "other", "role": "OTHER"},
    "Trouble in Pairs": {"cost": "2WW", "type": "enchantment", "role": "OTHER"},
    "Underworld Breach": {"cost": "1R", "type": "enchantment", "role": "OTHER"},
    "Vexing Bauble": {"cost": "1", "type": "artifact", "role": "OTHER"},
    "Voice of Victory": {"cost": "1W", "type": "other", "role": "OTHER"},
    "Wheel of Fortune": {"cost": "2R", "type": "sorcery", "role": "OTHER"},
    "Word of Seizing": {"cost": "3RR", "type": "instant", "role": "OTHER"},
}


class Card:
    """Clase objeto requerida por el motor para acceder a atributos como .role o .name"""

    def __init__(self, name, data):
        self.name = name
        self.role = data.get("role", "OTHER")
        self.type = data.get("type", "other")
        self.cost = data.get("cost", "1")
        self.is_monolith = data.get("is_monolith", False)
        self.is_outlet = data.get("is_outlet", False)
        self.is_fetch = data.get("is_fetch", False)
        self.mana_added = data.get("mana_added", {})
        self.produces = data.get("produces", [])

        # Asignar cualquier otro atributo adicional
        for key, value in data.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        return f"<Card: {self.name} ({self.role})>"


def get_card(card_name):
    """Retorna un objeto de la clase Card estructurado"""
    card_data = CARDS_DATABASE.get(
        card_name, {"cost": "1", "type": "other", "role": "OTHER"}
    )
    return Card(card_name, card_data)


# Alias por compatibilidad
get_card_info = get_card
