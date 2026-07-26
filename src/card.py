class Card:
    """Represents a Magic: The Gathering card with all relevant attributes for Zirdabilities simulation."""

    def __init__(
        self,
        name: str,
        card_type: str,
        role: str,
        cost_generic: int = 0,
        cost_pips: dict = None,
        mana_produced: dict = None,
        is_ephemeral: bool = False,
        restrictions: list = None,
    ):
        self.name = name
        self.card_type = (
            card_type  # Land, Artifact, Instant, Sorcery, Creature, Enchantment
        )
        self.role = (
            role  # Land, Mana_Rock, Ritual, Tutor, Piece, Outlet, Other
        )
        self.cost_generic = cost_generic
        self.cost_pips = (
            cost_pips if cost_pips else {"R": 0, "W": 0}
        )  # Color pips required
        self.mana_produced = (
            mana_produced if mana_produced else {"R": 0, "W": 0, "C": 0}
        )
        self.is_ephemeral = (
            is_ephemeral  # True if consumed upon use (Rituals, Lotus Petal, etc.)
        )
        self.restrictions = (
            restrictions if restrictions else []
        )  # Special mechanical conditions

    def __repr__(self):
        return f"<Card: {self.name} | Role: {self.role}>"
