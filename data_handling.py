import re
from pathlib import Path
import os

import pandas as pd

from data_constants import RAW_SIGNS, DOUBLE_SIGNS, SIGN2IDX, LEGARMEI, N_ROWS_PENTACOST
from utils import init_logger

LOGGER = None


def convert_word_to_signs(word):
    # Only keeping the signs
    signs = ''.join((filter(lambda c: c in RAW_SIGNS, word)))
    total_duplications_found = 0

    # Removing double signs
    for sign in DOUBLE_SIGNS:
        signs, dups = re.subn(f'{sign}{sign}', sign, signs)
        total_duplications_found += dups

    signs = list(map(SIGN2IDX.__getitem__, signs))

    if SIGN2IDX[chr(0x05A3)] in signs and chr(0x05C0) in word:
        # Munach + Paseq
        signs.remove(SIGN2IDX[chr(0x05A3)])
        signs.append(SIGN2IDX[LEGARMEI])
        total_duplications_found += 1

    # More exceptions to take care of:
    # - When Pashta appear twice, the first appearance is Kadma
    # - When Zarka appears twice, it does so as two different signs
    # - Generalize the above two cases together with the Munach + Paseq case.
    # - Collapse the two signs for Geresh (11 + 12) into a single one.

    LOGGER.info(f'Replaced {total_duplications_found} signs (double or special cases).')

    return signs


def create_teamim_df(config):
    path = Path(config['raw_path'])
    output_dir = Path(config['output_dir'])

    # Names to give to the columns
    columns = ['book', 'chapter', 'verse', 'raw_word']

    # Reading the data file into a DataFrame object.
    df = pd.read_csv(path, delim_whitespace=True, header=None, names=columns, encoding='utf-8',
                     dtype={
                         'book': str,
                         'chapter': int,
                         'verse': int,
                         'raw_word': str
                     },
                     index_col=False,
                     nrows=N_ROWS_PENTACOST)

    # Apply the word->list of signs conversion function to each word.
    df['signs'] = df['raw_word'].apply(convert_word_to_signs)

    # Group by the distinct verses and concatenate it all together
    verse_groups = df.groupby(by=['book', 'chapter', 'verse'])
    df = verse_groups.signs.aggregate(lambda l: [item for sublist in l for item in sublist]).reset_index()
    # df = pd.DataFrame(df.to_records())

    if config.get('save_verses', False):
        output_dir.mkdir(exist_ok=True, parents=True)
        df.to_csv(output_dir / f'parsed_verses.csv', index_label='index', index=True, header=True)
    return df


def get_teamim_df(config):
    output_dir = Path(config['output_dir'])

    if os.path.isfile(output_dir/f'parsed_verses.csv'):
        df = pd.read_csv(output_dir/f'parsed_verses.csv', index_col='index')
    else:
        df = create_teamim_df(config)

    return df


if __name__ == '__main__':
    # global LOGGER
    LOGGER = init_logger('data_handling', 'logs', to_screen=False)
    dirpath = os.path.dirname(__file__)
    config = {
        'raw_path': os.path.join(dirpath, 'data', 'word_by_word.txt'),
        'output_dir': os.path.join(dirpath, 'data'),
        'save_verses': True
    }

    print(SIGN2IDX)

    df = get_teamim_df(config)
    print(df[df['book'] == 'Gen'].head())
