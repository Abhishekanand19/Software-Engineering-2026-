"""Lab 6: tests exercising every executable statement of atm_withdrawal.py."""

import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


def test_withdrawal_own_bank():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_unknown_account():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "business", True)


def test_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 150, "savings", True)


def test_daily_limit_exceeded():
    assert withdraw(50000, 30000, "savings", True) == "limit exceeded"


def test_other_bank_large_withdrawal_extra_fee():
    assert withdraw(20000, 15000, "savings", False) == 4970


def test_insufficient_funds_including_fee():
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


def test_pin_attempts_exceeded():
    assert pin_check(1111, 1234, 3) == "card blocked"


def test_pin_correct():
    assert pin_check(1234, 1234, 0) == "ok"


def test_pin_last_failed_attempt():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_pin_retry():
    assert pin_check(1111, 1234, 0) == "retry"


def test_invalid_note_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(750)


def test_notes_with_two_hundred():
    assert note_breakup(800) == (1, 1, 1)


def test_notes_without_two_hundred():
    assert note_breakup(600) == (1, 0, 1)
