N_ROWS_PENTACOST = 80758

RAW_SIGN_CODES = list(range(0x0591, 0x05AF)) + [0x05BD]
RAW_SIGNS = [chr(c) for c in RAW_SIGN_CODES]

# Signs that may appear twice on the same word without duplicating the meaning
DOUBLE_SIGN_CODES = [0x0599, 0x05AE, 0x0592, 0x05A0, 0x05A9]
DOUBLE_SIGNS = list(map(chr, DOUBLE_SIGN_CODES))

# Special symbol for munach-legarmei
LEGARMEI = '[LEGARMEI]'

SPECIAL_SIGNS = [LEGARMEI]

ALL_SIGNS = RAW_SIGNS + SPECIAL_SIGNS

# Mapping from sign to index
SIGN2IDX = {sign: ind for ind, sign in enumerate(ALL_SIGNS)}
