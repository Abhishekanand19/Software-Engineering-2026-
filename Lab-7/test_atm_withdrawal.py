"""Hypothesis fuzz tests for all three ATM functions (Lab 7)."""

from hypothesis import given, settings, strategies as st
import pytest

from atm_withdrawal import notes_needed, mask_card, average_withdrawal


FUZZ = settings(max_examples=100, deadline=None, derandomize=True, database=None)


@FUZZ
@given(st.text(max_size=100) | st.none())
def test_notes_needed_no_crash(s):
    result = notes_needed(s)
    assert type(result) is int
    assert result >= 0


@FUZZ
@given(st.text(max_size=100) | st.none())
def test_mask_card_no_crash(s):
    result = mask_card(s)
    assert isinstance(result, str)
    assert result == "Invalid card number" or result.startswith("XXXX XXXX XXXX ")


@FUZZ
@given(st.text(max_size=100) | st.none())
def test_average_withdrawal_no_crash(s):
    result = average_withdrawal(s)
    assert type(result) is int
    assert result >= 0


@FUZZ
@given(st.integers(min_value=0, max_value=1_000_000))
def test_notes_needed_valid_amount(n):
    assert notes_needed(f"{n:,}") == n // 100


@FUZZ
@given(st.text(alphabet="0123456789", min_size=16, max_size=16))
def test_mask_card_keeps_only_last_four(digits):
    spaced = " ".join(digits[i:i+4] for i in range(0, 16, 4))
    assert mask_card(spaced) == "XXXX XXXX XXXX " + digits[-4:]


@FUZZ
@given(st.lists(st.integers(min_value=0, max_value=100_000), min_size=1, max_size=20))
def test_average_withdrawal_valid_csv(values):
    csv = ",".join(str(n) for n in values)
    assert average_withdrawal(csv) == sum(values) // len(values)


@pytest.mark.parametrize("bad", ["", "abc", "1,2,3", "-100", "1.5", None])
def test_notes_needed_invalid_returns_zero(bad):
    assert notes_needed(bad) == 0


@pytest.mark.parametrize("bad", ["", "1234", "1234 5678", "0000 0000 0000 XXXX", None])
def test_mask_card_invalid_returns_message(bad):
    assert mask_card(bad) == "Invalid card number"


@pytest.mark.parametrize("bad", ["", "100,,300", "100,hello", "-100,200", None])
def test_average_invalid_returns_zero(bad):
    assert average_withdrawal(bad) == 0
