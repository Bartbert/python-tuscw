class Attacker:

    def __init__(self):
        self.sp_count = 1
        self.leader_modifier = 0
        self.naval_support = False
        self.special_action = False
        self.is_demoralized = False

    def get_die_roll_modifier(self):
        drm = self.leader_modifier

        if self.is_demoralized:
            drm -= 2

        if self.special_action:
            drm += 2

        if self.naval_support:
            drm += 1

        return drm


class Defender:

    def __init__(self):
        self.sp_count = 1
        self.leader_modifier = 0
        self.naval_support = False
        self.defending_behind_mountain = False
        self.defending_behind_river = False
        self.fortification_modifier = 0
        self.is_foraging = False

    def get_die_roll_modifier(self):
        drm = self.leader_modifier

        if self.naval_support:
            drm += 1

        river_defense = 0
        if self.defending_behind_river:
            river_defense = 1

        mountain_defense = 0
        if self.defending_behind_mountain:
            mountain_defense = 1

        drm += max(river_defense, mountain_defense, self.fortification_modifier)

        return drm
