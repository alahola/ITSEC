'''
@author: Christian Wressnegger
'''

import os
MY_DIR = os.path.dirname(os.path.abspath(__file__))

MONO = {
    "encrypt": [
        ("abcdefghijklmnopqrstuvwxyz", b"Exercise 01", b"exercise"),
        ("vyjlnfubidxaqmshprwkgeoztc",
         b"Security exercises are fun", b"wnjgriktnznrjiwnwvrnfgm")
    ],
    "decrypt": [
        ("vyjlnfubidxaqmshprwkgeoztc",
         b"wnjgriktnznrjiwnwvrnfgm", b"securityexercisesarefun")
    ]
}

BREAK_MONO = {
    (os.path.join(MY_DIR, 'ex01_mono.plaintext'),
     os.path.join(MY_DIR, 'ex01_mono.ciphertext'))
}

VIG = {
    "encrypt": [
        ("abcdefghijklmnopqrstuvwxyz", b"Exercise 01", b"eygugnyl"),
        ("mono",
         b"Security exercises are fun", b"kienljlqizxldakiutlfxmr")
    ],
    "decrypt": [
        ("mono",
         b"kienljlqizxldakiutlfxmr", b"securityexercisesarefun")
    ]
}

BREAK_VIG = {
    (os.path.join(MY_DIR, 'ex01_vig.plaintext'),
     os.path.join(MY_DIR, 'ex01_vig.ciphertext'))
}

BREAK_VIG_KEYLEN = 5

TOOL_MAP = {"mono/mono.py": MONO, "mono/break_mono.py": BREAK_MONO,
            "vigenere/vig.py": VIG, "vigenere/break_vig.py": BREAK_VIG}
