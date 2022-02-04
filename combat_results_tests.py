import pytest

import combat_results as cr
import combatant


@pytest.mark.parametrize("sp_count_value, expected_result", [
    (0, 0.0), (1, 0.0), (2, 0.25), (3, 0.25), (4, 0.5), (5, 0.5),
    (7, 1.0), (8, 1.0),
    (9, 1.0), (10, 1.0), (11, 1.0), (12, 1.0),
    (13, 1.25), (14, 1.25), (15, 1.25), (16, 1.25),
    (17, 1.5), (18, 1.5)
])
def test_crt_results_sp_counts(sp_count_value, expected_result):
    crt = cr.CombatResultsTable()

    attacker = combatant.Attacker()
    attacker.sp_count = sp_count_value
    attacker.leader_modifier = 0

    attacker = crt.get_result(attacker, die_roll=1)

    assert attacker.result == expected_result


@pytest.mark.parametrize("sp_count_value, die_roll, expected_result", [
    (0, 1, 0.00), (0, 2, 0.00), (0, 3, 0.25), (0, 4, 0.25), (0, 5, 0.50), (0, 6, 0.50), (0, 7, 1.00), (0, 8, 1.00),
    (6, 1, 0.50), (6, 2, 1.00), (6, 3, 1.00), (6, 4, 1.00), (6, 5, 1.50), (6, 6, 1.50), (6, 7, 2.00), (6, 8, 2.00),
    (7, 1, 1.00), (7, 4, 1.00), (7, 6, 1.25), (7, 8, 1.50), (7, 9, 1.50), (7, 11, 2.00), (7, 13, 2.00), (7, 15, 3.00),
    (12, 1, 1.00), (12, 4, 1.25), (12, 6, 1.50), (12, 8, 1.50), (12, 9, 2.00), (12, 11, 2.00), (12, 13, 3.00),
    (12, 15, 3.00),
    (13, 1, 1.25), (13, 6, 1.50), (13, 9, 1.50), (13, 11, 2.00), (13, 13, 2.00), (13, 16, 3.00), (13, 19, 3.00),
    (13, 22, 4.00),
    (17, 1, 1.50), (17, 6, 1.50), (17, 9, 2.00), (17, 11, 2.00), (17, 13, 3.00), (17, 16, 3.00), (17, 19, 4.00),
    (17, 22, 4.00),
])
def test_crt_results_die_rolls(sp_count_value, die_roll, expected_result):
    crt = cr.CombatResultsTable()

    attacker = combatant.Attacker()
    attacker.sp_count = sp_count_value
    attacker.leader_modifier = 0

    attacker = crt.get_result(attacker, die_roll=die_roll)

    assert attacker.result == expected_result


@pytest.mark.parametrize("leader_mod, expected_result", [
    (1, 1.00), (2, 1.00), (3, 1.00), (4, 1.25), (5, 1.25), (6, 1.50), (7, 1.50),
    (8, 1.50), (9, 2.00), (10, 2.00), (11, 2.00), (12, 2.00), (13, 3.00), (14, 3.00)
])
def test_crt_results_leader_mod(leader_mod, expected_result):
    crt = cr.CombatResultsTable()

    attacker = combatant.Attacker()
    attacker.sp_count = 7
    attacker.leader_modifier = leader_mod

    attacker = crt.get_result(attacker, die_roll=2)

    assert attacker.result == expected_result


def test_drm_demoralized():
    attacker = combatant.Attacker()
    attacker.sp_count = 7
    attacker.is_demoralized = True

    assert attacker.get_die_roll_modifier() == -2


def test_drm_leader_mod():
    attacker = combatant.Attacker()
    attacker.sp_count = 7
    attacker.leader_modifier = 2

    assert attacker.get_die_roll_modifier() == 2


def test_drm_special_action():
    attacker = combatant.Attacker()
    attacker.sp_count = 7
    attacker.special_action = True

    assert attacker.get_die_roll_modifier() == 2


def test_drm_naval_support():
    attacker = combatant.Attacker()
    attacker.sp_count = 7
    attacker.naval_support = True

    assert attacker.get_die_roll_modifier() == 1


def test_drm_entrenchment():
    defender = combatant.Defender()
    defender.sp_count = 7
    defender.fortification_modifier = 2

    assert defender.get_die_roll_modifier() == 2
