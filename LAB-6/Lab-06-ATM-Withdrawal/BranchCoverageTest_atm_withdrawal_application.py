"""Lab 6: boundary and decision tests for full branch coverage."""

import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


@pytest.mark.parametrize("balance, amount, account_type, own_bank, expected", [
    (5000, 1000, "savings", True, 4000),           # Own bank: no fee
    (5000, 1000, "savings", False, 3980),          # Other bank: Rs.20 fee
    (20000, 10000, "savings", False, 9980),       # Exactly Rs.10,000: no extra fee
    (20000, 10100, "savings", False, 9870),       # Above Rs.10,000: Rs.30 fee
    (1000, 1000, "savings", False, "insufficient funds"),
    (1020, 1000, "savings", False, 0),            # Exact balance including fee
    (24999, 25000, "savings", True, "insufficient funds"),
    (25000, 25000, "savings", True, 0),            # Savings daily limit boundary
    (30000, 25100, "savings", True, "limit exceeded"),
    (50000, 50000, "current", True, 0),            # Current-account boundary
    (60000, 50100, "current", True, "limit exceeded"),
])
def test_withdrawal_decisions(balance, amount, account_type, own_bank, expected):
    assert withdraw(balance, amount, account_type, own_bank) == expected


@pytest.mark.parametrize("amount, account_type, error", [
    (1000, "business", "unknown account"),
    (0, "savings", "invalid amount"),             # amount <= 0 is True
    (-100, "current", "invalid amount"),
    (150, "savings", "invalid amount"),           # amount % 100 != 0 is True
])
def test_withdrawal_invalid_input(amount, account_type, error):
    with pytest.raises(ValueError, match=error):
        withdraw(60000, amount, account_type, True)


@pytest.mark.parametrize("entered, actual, attempts, expected", [
    (1111, 1234, 3, "card blocked"),               # Already blocked
    (1234, 1234, 0, "ok"),
    (1111, 1234, 2, "card blocked"),               # Third incorrect PIN
    (1111, 1234, 0, "retry"),
    (1111, 1234, 1, "retry"),
    (1234, 1234, 3, "card blocked"),               # Block check precedes PIN check
])
def test_pin_decisions(entered, actual, attempts, expected):
    assert pin_check(entered, actual, attempts) == expected


@pytest.mark.parametrize("amount, expected", [
    (100, (0, 0, 1)),                              # No Rs.200 notes
    (200, (0, 1, 0)),                              # Rs.200 branch
    (400, (0, 2, 0)),
    (500, (1, 0, 0)),
    (600, (1, 0, 1)),
    (800, (1, 1, 1)),
])
def test_note_breakup_decisions(amount, expected):
    assert note_breakup(amount) == expected


def test_note_breakup_rejects_non_multiples_of_100():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(750)
