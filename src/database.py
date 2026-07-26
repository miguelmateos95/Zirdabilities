# ==============================================================================
# BASE DE DATOS COMPLETA DE CARTAS (ZIRDA SIMULATION)
# Contiene tanto la base previa del motor como las nuevas cartas incorporadas.
# ==============================================================================

CARDS_DATABASE = {
    # --------------------------------------------------------------------------
    # 1. PIEZAS CORE DEL COMBO (EXISTENTES)
    # --------------------------------------------------------------------------
    "Basalt Monolith": {
        "cost": "3",
        "type": "artifact",
        "is_monolith": True,
        "mana_produced": 3,
        "untap_cost": 3,  # Se reduce a 1 con Zirda en mesa -> Genera mana infinito
    },
    "Grim Monolith": {
        "cost": "2",
        "type": "artifact",
        "is_monolith": True,
        "mana_produced": 3,
        "untap_cost": 4,  # Se reduce a 2 con Zirda en mesa -> Genera mana infinito
    },
    "Monolith": {  # Alias genérico para soporte del motor
        "cost": "3",
        "type": "artifact",
        "is_monolith": True,
    },
    
    # Outlets / Condición de Victoria Previos
    "Walking Ballista": {"cost": "XX", "type": "artifact_creature", "is_outlet": True},
    "Staff of Domination": {"cost": "3", "type": "artifact", "is_outlet": True, "activated_ability_cost": "1"},
    "Diviner's Wand": {"cost": "3", "type": "artifact", "is_outlet": True, "activated_ability_cost": "4"},
    "Sanctum of Eternity": {"type": "land", "produces": ["C"], "is_outlet": True},

    # Fast Mana Base Previos
    "Sol Ring": {"cost": "1", "type": "artifact", "mana_added": {"C": 2}},
    "Mana Crypt": {"cost": "0", "type": "artifact", "mana_added": {"C": 2}},
    "Mana Vault": {"cost": "1", "type": "artifact", "mana_added": {"C": 3}},
    "Mox Diamond": {"cost": "0", "type": "artifact", "mana_added": {"any": 1}},
    "Chrome Mox": {"cost": "0", "type": "artifact", "mana_added": {"any": 1}},
    "Lotus Petal": {"cost": "0", "type": "artifact", "mana_added": {"any": 1}},
    "Arcane Signet": {"cost": "2", "type": "artifact", "mana_added": {"R": 1, "W": 1}},
    "Boros Signet": {"cost": "2", "type": "artifact", "mana_added": {"R": 1, "W": 1}},
    "Talisman of Conviction": {"cost": "2", "type": "artifact", "mana_added": {"R": 1, "W": 1}},

    # --------------------------------------------------------------------------
    # 2. NUEVAS TIERRAS Y MANÁ BASE
    # --------------------------------------------------------------------------
    "Arid Mesa": {"type": "land", "produces": ["R", "W"], "is_fetch": True},
    "Bloodstained Mire": {"type": "land", "produces": ["R", "W"], "is_fetch": True},
    "Marsh Flats": {"type": "land", "produces": ["R", "W"], "is_fetch": True},
    "Wooded Foothills": {"type": "land", "produces": ["R", "W"], "is_fetch": True},
    
    "Battlefield Forge": {"type": "land", "produces": ["C", "R", "W"]},
    "City of Brass": {"type": "land", "produces": ["R", "W"]},
    "Command Tower": {"type": "land", "produces": ["R", "W"]},
    "Exotic Orchard": {"type": "land", "produces": ["R", "W"]},
    "Great Furnace": {"type": "land", "produces": ["R"], "is_artifact": True},
    "Mana Confluence": {"type": "land", "produces": ["R", "W"]},
    "Mountain": {"type": "land", "produces": ["R"]},
    "Plains": {"type": "land", "produces": ["W"]},
    "Plateau": {"type": "land", "produces": ["R", "W"]},
    "Sacred Foundry": {"type": "land", "produces": ["R", "W"]},
    "Spectator Seating": {"type": "land", "produces": ["R", "W"]},
    "Starting Town": {"type": "land", "produces": ["R", "W"]},
    "Sunbaked Canyon": {"type": "land", "produces": ["R", "W"]},

    # Tierras Especiales
    "Emergence Zone": {"type": "land", "produces": ["C"]},
    "Treasure Vault": {"type": "land", "produces": ["C"], "is_artifact": True},
    "Abstergo Entertainment": {
        "type": "land",
        "produces": ["C"],
        "filter_ability": True  # Lógica: Genera 1C o filtra 1C -> 1R/1W
    },
    "Spire of Industry": {
        "type": "land",
        "produces_conditional": lambda state: ["R", "W"] if state.artifacts_count > 0 else ["C"]
    },
    "Inventors' Fair": {
        "type": "land",
        "produces": ["C"],
        "can_tutor_artifact": lambda state: state.artifacts_count >= 3
    },

    # --------------------------------------------------------------------------
    # 3. NUEVO MANA FAST, RITUALES Y OUTLETS
    # --------------------------------------------------------------------------
    "_____ Goblin": {
        "cost": "2R",
        "type": "ritual",
        "mana_added": {"R": 5}  # Media configurada
    },
    "Treasonous Ogre": {
        "cost": "3R",
        "type": "creature",
        "pay_life_for_mana": {"R": 10}
    },
    "Lion's Eye Diamond": {
        "cost": "0",
        "type": "artifact",
        "is_led": True,
        "cast_condition": lambda state: state.has_monolith_and_outlet_in_play()
    },
    "Kozilek's Command": {"cost": "XCC", "type": "instant", "is_outlet": True},
    "Thran Spider": {"cost": "3", "type": "artifact_creature", "is_outlet": True, "activated_ability_cost": "7"},
    
    # --------------------------------------------------------------------------
    # 4. SINTERGIA DE ARTEFACTOS Y MOTOR DE ROBOS
    # --------------------------------------------------------------------------
    "Rings of Brighthearth": {"cost": "3", "type": "artifact", "combo_piece": True},
    "Manifold Key": {"cost": "1", "type": "artifact", "untap_synergy": True},
    "Voltaic Key": {"cost": "1", "type": "artifact", "untap_synergy": True},
    "Mirage Mirror": {"cost": "3", "type": "artifact", "utility": True},
    "Scroll Rack": {"cost": "2", "type": "artifact", "draw_engine": True},
    "The One Ring": {"cost": "4", "type": "artifact", "draw_engine": True},
    "Goblin Engineer": {"cost": "1R", "type": "creature", "tutor_artifact": True},
    "Oswald Fiddlebender": {"cost": "1W", "type": "creature", "tutor_artifact": True},

    # --------------------------------------------------------------------------
    # 5. RESTO DE CARTAS (INTERRUPCIÓN, UTILITY, STAX, PROTECCIÓN)
    # --------------------------------------------------------------------------
    "Archivist of Oghma": {"cost": "1W", "type": "other"},
    "Black Widow, Agile Avenger": {"cost": "1R", "type": "other"},
    "Borrowed Knowledge": {"cost": "1W", "type": "other"},
    "Deflecting Swat": {"cost": "0", "type": "instant"},
    "Delivery Moogle": {"cost": "2W", "type": "other"},
    "Drannith Magistrate": {"cost": "1W", "type": "other"},
    "Esper Sentinel": {"cost": "W", "type": "other"},
    "Ethersworn Canonist": {"cost": "1W", "type": "other"},
    "Final Fortune": {"cost": "RR", "type": "instant"},
    "Hex Magic": {"cost": "1R", "type": "other"},
    "Jolted Awake": {"cost": "W", "type": "other"},
    "Liberator, Urza's Battlethopter": {"cost": "3", "type": "other"},
    "Orim's Chant": {"cost": "W", "type": "instant"},
    "Portable Hole": {"cost": "W", "type": "other"},
    "Pyroblast": {"cost": "R", "type": "instant"},
    "Ragavan, Nimble Pilferer": {"cost": "R", "type": "creature"},
    "Recommission": {"cost": "1W", "type": "other"},
    "Red Elemental Blast": {"cost": "R", "type": "instant"},
    "Redirect Lightning": {"cost": "1R", "type": "instant"},
    "Sevinne's Reclamation": {"cost": "2W", "type": "other"},
    "Silence": {"cost": "W", "type": "instant"},
    "Smothering Tithe": {"cost": "3W", "type": "enchantment"},
    "Swords to Plowshares": {"cost": "W", "type": "instant"},
    "Tataru Taru": {"cost": "1W", "type": "other"},
    "Touch the Spirit Realm": {"cost": "2W", "type": "other"},
    "Trouble in Pairs": {"cost": "2WW", "type": "enchantment"},
    "Underworld Breach": {"cost": "1R", "type": "enchantment"},
    "Vexing Bauble": {"cost": "1", "type": "artifact"},
    "Voice of Victory": {"cost": "1W", "type": "other"},
    "Wheel of Fortune": {"cost": "2R", "type": "sorcery"},
    "Word of Seizing": {"cost": "3RR", "type": "instant"},
}


def get_card_info(card_name):
    """
    Función de búsqueda rápida en el motor.
    Si una carta no está explícitamente en el diccionario, se devuelve como 'OTHER'
    para evitar detención de ejecución.
    """
    return CARDS_DATABASE.get(card_name, {"cost": "1", "type": "other"})
