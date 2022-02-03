import combat_results as cr
import combatant


def print_hi():
    crt = cr.CombatResultsTable()
    print(crt.crt_1)

    attacker = combatant.Attacker()
    attacker.sp_count = 3
    attacker.leader_modifier = 0
    print(f'\nAttacker SP Count: {attacker.sp_count}')

    defender = combatant.Defender()
    defender.sp_count = 2
    defender.leader_modifier = 0

    attacker = crt.get_result(attacker, 3)
    print(f'Die Roll = {attacker.die_roll}')
    print(f'Result: {attacker.result}')

    print(crt.single_die)
    print(crt.two_dice)
    print(crt.three_dice)

    print(sum(crt.two_dice.values()))
    print(crt.two_dice.get(7) / sum(crt.two_dice.values()))

    df = crt.analyze_combat(attacker, defender)
    print(df)
    print(sum(df.loc[df['battle_result'] == 'attacker_victory']['combined_probability']))
    print(sum(df.loc[df['battle_result'] == 'defender_victory']['combined_probability']))
    print(sum(df.loc[df['battle_result'] == 'tie']['combined_probability']))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
