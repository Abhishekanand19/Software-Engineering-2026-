def evaluate(target, guess):
    if len(target) != len(guess):
        raise ValueError("Target and guess must have the same length.")

    result = ["gray"] * len(guess)
    remaining = {}
    for i, ch in enumerate(guess):
        if ch == target[i]:
            result[i] = "green"
        else:
            letter = target[i]
            remaining[letter] = remaining.get(letter, 0) + 1
    for i, ch in enumerate(guess):
        if result[i] == "green":
            continue
        if remaining.get(ch, 0):
            result[i] = "yellow"
            remaining[ch] -= 1
    return result
