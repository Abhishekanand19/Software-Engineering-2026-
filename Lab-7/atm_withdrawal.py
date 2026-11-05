"""Hardened ATM withdrawal helpers for Lab 7.

Invalid inputs return safe defaults instead of raising exceptions:
* notes_needed -> 0
* mask_card -> "Invalid card number"
* average_withdrawal -> 0

These are explicit lab-level policies; a production banking application
should raise structured validation errors and reject invalid transactions.
"""

import re


_AMOUNT = re.compile(r"(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)")
_CARD = re.compile(r"[0-9 -]+")
_CSV_AMOUNT = re.compile(r"[0-9]{1,18}")


def notes_needed(amount):
    """Count complete 100-value notes in a nonnegative whole-number amount."""
    if not isinstance(amount, str):
        return 0

    cleaned = amount.strip()
    if not cleaned or not _AMOUNT.fullmatch(cleaned):
        return 0

    digits = cleaned.replace(",", "")
    if len(digits) > 18:
        return 0

    return int(digits) // 100


def mask_card(card_number):
    """Mask a 16-digit card, tolerating spaces or hyphens as separators."""
    if not isinstance(card_number, str):
        return "Invalid card number"

    cleaned = card_number.strip()
    if not cleaned or not _CARD.fullmatch(cleaned):
        return "Invalid card number"

    digits = cleaned.replace(" ", "").replace("-", "")
    if len(digits) != 16:
        return "Invalid card number"

    return "XXXX XXXX XXXX " + digits[-4:]


def average_withdrawal(amounts_csv):
    """Calculate the floored mean of nonnegative whole-number CSV amounts."""
    if not isinstance(amounts_csv, str) or not amounts_csv.strip():
        return 0

    parts = amounts_csv.split(",")
    # Keep parsing bounded even for untrusted, extremely large input strings.
    if len(parts) > 1000:
        return 0

    stripped = [part.strip() for part in parts]
    if any(not _CSV_AMOUNT.fullmatch(part) for part in stripped):
        return 0

    values = [int(part) for part in stripped]
    return sum(values) // len(values)


def main():
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")
    print("Number of 100 Notes:", notes_needed(user_input))

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")
    print("Masked Card:", mask_card(user_input))

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")
    print("Average Withdrawal:", average_withdrawal(user_input))


if __name__ == "__main__":
    main()
