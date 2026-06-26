"""
A Friendly Command-Line Password Generator
--------------------------------------------
"""

import random
import string


def ask_yes_no(message):
    """Keep asking until the user answers y or n."""
    while True:
        answer = input(message).strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("Please answer with 'y' or 'n'.")


def get_length():
    """Keep asking until the user gives a sensible length."""
    while True:
        try:
            length = int(input("How long should the password be? (4-50): "))
            if 4 <= length <= 50:
                return length
            print("Pick a length between 4 and 50.")
        except ValueError:
            print("That's not a number. Try again!")


def build_character_pool(use_upper, use_lower, use_digits, use_symbols):
    """Combine the chosen character sets into one pool."""
    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += "!@#$%^&*()-_=+?"
    return pool


def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """Build a password guaranteeing at least one of each chosen type."""
    pool = build_character_pool(use_upper, use_lower, use_digits, use_symbols)

    # Start with one guaranteed character from each selected type
    password_chars = []
    if use_upper:
        password_chars.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password_chars.append(random.choice(string.ascii_lowercase))
    if use_digits:
        password_chars.append(random.choice(string.digits))
    if use_symbols:
        password_chars.append(random.choice("!@#$%^&*()-_=+?"))

    # Fill the rest randomly from the full pool
    while len(password_chars) < length:
        password_chars.append(random.choice(pool))

    # Shuffle so the guaranteed characters aren't always at the front
    random.shuffle(password_chars)
    return "".join(password_chars[:length])


def rate_strength(length, type_count):
    """A simple score based on length and variety of character types."""
    score = length + (type_count * 5)
    if score < 12:
        return "Weak", "*"
    elif score < 20:
        return "Okay", "**"
    elif score < 30:
        return "Strong", "***"
    else:
        return "Very Strong", "****"


def draw_meter(stars):
    """Turn star rating into a simple bar."""
    filled = len(stars)
    return "[" + "#" * filled + "-" * (4 - filled) + "]"


def main():
    print("=" * 50)
    print(" PASSWORD GENERATOR ")
    print("=" * 50)

    while True:
        length = get_length()

        print("\nWhich character types should be included?")
        use_upper = ask_yes_no("Include UPPERCASE letters? (y/n): ")
        use_lower = ask_yes_no("Include lowercase letters? (y/n): ")
        use_digits = ask_yes_no("Include digits (0-9)? (y/n): ")
        use_symbols = ask_yes_no("Include symbols (!@#$...)? (y/n): ")

        type_count = sum([use_upper, use_lower, use_digits, use_symbols])
        if type_count == 0:
            print("\nYou need to pick at least one character type!\n")
            continue

        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        strength, stars = rate_strength(length, type_count)

        print("\n" + "-" * 50)
        print(f"Your password: {password}")
        print(f"Strength: {strength} {draw_meter(stars)}")
        print("-" * 50)

        again = ask_yes_no("\nGenerate another password? (y/n): ")
        if not again:
            print("\nThanks for using the Password Generator. Stay secure!")
            break


if __name__ == "__main__":
    main()