import random
import string

def get_random_string(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])

def get_random_string_with_symbol(length):
    return ''.join([random.choice(string.ascii_letters + string.digits + '_' + '-' + '!' + '#' + '&') for i in range(length)])
