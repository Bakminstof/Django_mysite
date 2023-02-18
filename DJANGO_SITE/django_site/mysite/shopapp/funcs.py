import random
import string

from typing import Dict


# Random generic
def gen_random_word(first_uppercase: bool = False) -> str:
    additional_letters_count = random.choice(range(3, 10))
    additional_letters = random.choices(string.ascii_lowercase, k=additional_letters_count)

    if first_uppercase:
        first_letter = random.choice(string.ascii_uppercase)
        word = first_letter + ''.join(additional_letters)
    else:
        word = ''.join(additional_letters)

    return word


def gen_random_price() -> float:
    first_digit = random.choice(string.digits[1:])
    price_length = random.choice(range(3, 7))
    digits = random.choices(string.digits, k=price_length)

    price = str(first_digit) + ''.join(digits)

    return float(price)


def gen_random_desc() -> str:
    additional_words_count = random.choice(range(10, 31))

    first_word = gen_random_word(first_uppercase=True)
    additional_words = [gen_random_word() for _ in range(additional_words_count)]

    descr = first_word + ' ' + ' '.join(additional_words)
    return descr


def gen_random_item() -> Dict[str, float | int | str]:
    item = {
        'name': gen_random_word(first_uppercase=True),
        'description': gen_random_desc() if random.choice((True, False)) else '',
        'price': gen_random_price()
    }

    return item
