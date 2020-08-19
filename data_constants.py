N_ROWS_PENTACOST = 80758

RAW_SIGN_CODES = list(range(0x0591, 0x05AF)) + [0x05BD]
RAW_SIGNS = [chr(c) for c in RAW_SIGN_CODES]

# Special symbol for munach-legarmei
LEGARMEI = '[LEGARMEI]'

SPECIAL_SIGNS = [LEGARMEI]

ALL_SIGNS = RAW_SIGNS + SPECIAL_SIGNS

# Mapping from sign to index
SIGN2IDX = {sign: ind for ind, sign in enumerate(ALL_SIGNS)}

# Signs that may appear twice on the same word without duplicating the meaning
DOUBLE_SIGN_CODES = [0x0592, 0x05A0, 0x05A9]
DOUBLE_SIGNS = list(map(chr, DOUBLE_SIGN_CODES))

DIFFERENT_MEANING_PAIRS = {(sign, sign): sign for sign in DOUBLE_SIGNS}
DIFFERENT_MEANING_PAIRS[(chr(0x05A3), chr(0x05C0))] = LEGARMEI
DIFFERENT_MEANING_PAIRS[(chr(0x05AB), chr(0x0599))] = chr(0x0599)
DIFFERENT_MEANING_PAIRS[(chr(0x0598), chr(0x05AE))] = chr(0x0599)
DIFFERENT_MEANING_PAIRS[(chr(0x059D),)] = chr(0x059C)
