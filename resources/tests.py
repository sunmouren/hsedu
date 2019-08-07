from django.test import TestCase

# Create your tests here.

text = 'what are you name?'

chars = tuple(set(text))

print(chars)

int2char = dict(enumerate(chars))

print(int2char)

char2int = {ch: ii for ii, ch in int2char.items()}

print(char2int)

# encode =