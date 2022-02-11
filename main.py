import combat_results as cr
import combatant
import pandas as pd


def print_hi():
    crt = cr.CombatResultsTable()
    print(crt.crt_1)

    attacker = combatant.Attacker()
    attacker.sp_count = 10
    attacker.leader_modifier = 0
    print(f'\nAttacker SP Count: {attacker.sp_count}')

    defender = combatant.Defender()
    defender.sp_count = 10
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

    df_stats = df.groupby(['battle_result'], as_index=False)[
        'combined_probability'].sum()
    print(df_stats)

    df_losses_atk = df.groupby(['attacker_losses'], as_index=False)['combined_probability'].sum()
    df_losses_atk = df_losses_atk.rename(columns={'attacker_losses': 'Losses'})
    df_losses_atk['combatant'] = 'Attacker'
    print(df_losses_atk)

    df_losses_def = df.groupby(['defender_losses'], as_index=False)['combined_probability'].sum()
    df_losses_def = df_losses_def.rename(columns={'defender_losses': 'Losses'})
    df_losses_def['combatant'] = 'Defender'
    print(df_losses_def)

    df_losses = pd.concat([df_losses_atk, df_losses_def], ignore_index=True)
    print(df_losses)

    print(df_losses.loc[df_losses['combatant'] == 'Attacker']['Losses'])
    print(df_losses.loc[df_losses['combatant'] == 'Defender']['Losses'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
