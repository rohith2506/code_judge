'''
It contains all helper functions in it
'''

import math
import json
import requests

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)
