import pandas as pd
from itertools import product
from collections import Counter


def die_rolls_for_one_die():
    return Counter([1, 2, 3, 4, 5, 6])


def die_rolls_for_two_dice():
    die_combinations = product(die_rolls_for_one_die(), repeat=2)

    dice_sum = []
    for dice in die_combinations:
        dice_sum.append(sum(dice))

    return Counter(dice_sum)


def die_rolls_for_three_dice():
    die_combinations = product(die_rolls_for_one_die(), repeat=3)

    dice_sum = []
    for dice in die_combinations:
        dice_sum.append(sum(dice))

    return Counter(dice_sum)


class CombatResultsTable:

    def __init__(self):
        self.crt_1 = pd.read_csv('data/crt_1_leader.csv')
        self.crt_2 = pd.read_csv('data/crt_2_leaders.csv')
        self.crt_3 = pd.read_csv('data/crt_3_leaders.csv')
        self.single_die = die_rolls_for_one_die()
        self.two_dice = die_rolls_for_two_dice()
        self.three_dice = die_rolls_for_three_dice()

    def analyze_combat(self, attacker, defender):
        if attacker.sp_count <= 6:
            attacker.die_rolls = self.single_die
        elif attacker.sp_count in range(7, 12 + 1):
            attacker.die_rolls = self.two_dice
        elif attacker.sp_count >= 13:
            attacker.die_rolls = self.three_dice

        if defender.sp_count <= 6:
            defender.die_rolls = self.single_die
        elif defender.sp_count in range(7, 12 + 1):
            defender.die_rolls = self.two_dice
        elif defender.sp_count >= 13:
            defender.die_rolls = self.three_dice

        die_rolls = product(attacker.die_rolls.keys(), defender.die_rolls.keys())

        attacker_die_rolls = []
        attacker_results = []
        attacker_losses = []
        attacker_probabilities = []

        defender_die_rolls = []
        defender_results = []
        defender_losses = []
        defender_probabilities = []

        battle_results = []
        combined_probabilities = []

        for die_roll in die_rolls:
            attacker_die_roll = die_roll[0]
            defender_die_roll = die_roll[1]

            attacker_probability = attacker.die_rolls.get(attacker_die_roll) / sum(attacker.die_rolls.values())
            defender_probability = defender.die_rolls.get(defender_die_roll) / sum(defender.die_rolls.values())
            combined_probability = attacker_probability * defender_probability

            result_attacker = self.get_result(attacker, attacker_die_roll).result
            result_defender = self.get_result(defender, defender_die_roll).result

            if result_attacker > result_defender:
                battle_result = 'attacker_victory'
            elif result_defender > result_attacker:
                battle_result = 'defender_victory'
            else:
                battle_result = 'tie'

            attacker_die_rolls.append(attacker_die_roll)
            attacker_results.append(result_attacker)
            defender_losses.append(int(result_attacker))
            attacker_probabilities.append(attacker_probability)

            defender_die_rolls.append(defender_die_roll)
            defender_results.append(result_defender)
            attacker_losses.append(int(result_defender))
            defender_probabilities.append(defender_probability)

            battle_results.append(battle_result)
            combined_probabilities.append(combined_probability)

        results_data = {
            'attacker_die_roll': attacker_die_rolls,
            'attacker_result': attacker_results,
            'attacker_losses': attacker_losses,
            'attacker_probability': attacker_probabilities,
            'defender_die_roll': defender_die_rolls,
            'defender_result': defender_results,
            'defender_losses': defender_losses,
            'defender_probability': defender_probabilities,
            'battle_result': battle_results,
            'combined_probability': combined_probabilities
        }

        return pd.DataFrame(data=results_data)

    def get_result(self, combatant, die_roll):

        modified_die_roll = die_roll + combatant.get_die_roll_modifier()

        if combatant.sp_count <= 6:
            return self.get_result_crt_1(combatant, modified_die_roll)
        elif combatant.sp_count in range(7, 12 + 1):
            return self.get_result_crt_2(combatant, modified_die_roll)
        elif combatant.sp_count >= 13:
            return self.get_result_crt_3(combatant, modified_die_roll)

    def get_result_crt_1(self, combatant, die_roll):
        col_name = ''

        if combatant.sp_count == 0:
            col_name = 'sp_0'
        elif combatant.sp_count == 1:
            col_name = 'sp_1'
        elif combatant.sp_count == 2:
            col_name = 'sp_2'
        elif combatant.sp_count == 3:
            col_name = 'sp_3'
        elif combatant.sp_count == 4:
            col_name = 'sp_4'
        elif combatant.sp_count in [5, 6]:
            col_name = 'sp_5_6'

        result = self.crt_1.loc[(self.crt_1['1d6_roll_lower'] <= die_roll) & (self.crt_1['1d6_roll_upper'] >= die_roll)]

        combatant.die_roll = die_roll
        combatant.result = float(result[col_name])

        return combatant

    def get_result_crt_2(self, combatant, die_roll):
        col_name = ''

        if combatant.sp_count in range(7, 8 + 1):
            col_name = 'sp_7_8'
        elif combatant.sp_count in range(9, 12 + 1):
            col_name = 'sp_9_12'

        result = self.crt_2.loc[(self.crt_2['2d6_roll_lower'] <= die_roll) & (self.crt_2['2d6_roll_upper'] >= die_roll)]

        combatant.die_roll = die_roll
        combatant.result = float(result[col_name])

        return combatant

    def get_result_crt_3(self, combatant, die_roll):
        col_name = ''

        if combatant.sp_count in range(13, 16 + 1):
            col_name = 'sp_13_16'
        elif combatant.sp_count >= 17:
            col_name = 'sp_17_up'

        result = self.crt_3.loc[(self.crt_3['3d6_roll_lower'] <= die_roll) & (self.crt_3['3d6_roll_upper'] >= die_roll)]

        combatant.die_roll = die_roll
        combatant.result = float(result[col_name])

        return combatant
