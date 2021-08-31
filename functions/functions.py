import random
import string

def token_maker(token_length):
    lower_letters = string.ascii_lowercase
    digits = string.digits
    all_strings = lower_letters + digits
    token = "".join(random.choice(all_strings) for units in range(token_length))
    return token




