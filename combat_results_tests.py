import combat_results as cr
import combatant


def test_crt_1_results():
    crt = cr.CombatResultsTable()

    attacker = combatant.Attacker()
    attacker.sp_count = 4
    attacker.leader_modifier = 0

    attacker = crt.get_result(attacker)

    assert attacker.sp_count == 4
