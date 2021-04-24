import logging
import random


class Preferences:
    def __init__(self, min_length, max_length, upper_case, special_chars, numbers):
        self.min_length = min_length
        self.max_length = max_length
        self.upper_case = upper_case
        self.special_chars = special_chars
        self.numbers = numbers

    def get_all_fields(self):
        return self.min_length, self.max_length, self.upper_case, self.special_chars, self.numbers


def is_whitespace(c: str):
    return c in ['\t', '\n', '\r', '\v', '\f']


def is_printable(c: str):
    return 32 <= ord(c) < 127


def is_special(c: str):
    return not c.isalpha() and not c.isdigit() and not is_whitespace(c) and is_printable(c)


digits = [str(i) for i in range(10)]
alphabet = [chr(i + 97) for i in range(26)]
specials = [chr(i) for i in range(255) if is_special(chr(i))]


def check_password(password: str, preferences: Preferences):
    min_length, max_length, upper_case, special_chars, numbers = preferences.get_all_fields()

    if not min_length <= len(password) <= max_length:
        logging.error(f'Expected password length: from {min_length} to {max_length}, found: {len(password)}')
        return False

    has_upper_case, has_special_chars, has_numbers = False, False, False

    for c in password:
        if c in digits:
            has_numbers = True
        elif is_special(c):
            has_special_chars = True
        elif c.isupper():
            has_upper_case = True

    if upper_case and not has_upper_case:
        logging.error(f'Expected special characters: {upper_case}, found: {has_upper_case}')
        return False
    if numbers and not has_numbers:
        logging.error(f'Expected special characters: {numbers}, found: {has_numbers}')
        return False
    if special_chars and not has_special_chars:
        logging.error(f'Expected special characters: {special_chars}, found: {has_special_chars}')
        return False

    return True


def generate_password(preferences: Preferences):
    min_length, max_length, upper_case, special_chars, numbers = preferences.get_all_fields()

    pwd = []
    if upper_case:
        pwd.append(random.choice(alphabet).upper())
    if special_chars:
        pwd.append(random.choice(specials))
    if numbers:
        pwd.append(random.choice(digits))

    length = random.randint(min_length, max_length)

    if len(pwd) > max_length:
        logging.error(f'Could not generate password with the provided constraints')
        return

    for i in range(length - len(pwd)):
        char_type = random.randint(1, 3)

        # alpha
        if char_type == 1:
            curr = random.choice(alphabet)
            if random.choice([True, False]):
                curr = curr.upper()
            pwd.append(curr)
        # digit
        elif char_type == 2:
            pwd.append(random.choice(digits))
        # special character
        else:
            pwd.append(random.choice(specials))

    return ''.join(pwd)
