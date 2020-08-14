import re
from pathlib import Path
import os
import json

import pandas as pd

import data_constants
from data_constants import RAW_SIGNS, DOUBLE_SIGNS, LEGARMEI, N_ROWS_PENTACOST, DIFFERENT_MEANING_PAIRS
from utils import init_logger

LOGGER = None


def convert_word_to_signs(word):
    total_duplications_found = 0

    for pair, result in DIFFERENT_MEANING_PAIRS.items():
        if all(item in word for item in pair):
            word = list(filter(lambda x: x not in pair, word))
            word.append(result)
            total_duplications_found += 1

    # Only keeping the signs
    signs = list(map(data_constants.SIGN2IDX.__getitem__,
                     filter(lambda c: c in RAW_SIGNS, word)))

    LOGGER.info(f'Replaced {total_duplications_found} signs (double or special cases).')

    return signs


def remove_metagim(verse):
    sof_passuk = data_constants.SIGN2IDX[chr(0x05BD)]
    verse = list(filter(lambda x: x != sof_passuk, verse))
    verse.append(sof_passuk)
    return verse


def create_teamim_df(config):
    path = Path(config['raw_path'])
    output_dir = Path(config['output_dir'])

    if (output_dir / 'vocab.json').is_file():
        with open(output_dir / 'vocab.json', 'r') as f:
            data_constants.SIGN2IDX = json.load(f)

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
    df['signs'] = df['signs'].apply(remove_metagim)
    # df = pd.DataFrame(df.to_records())

    if config.get('save_verses', False):
        output_dir.mkdir(exist_ok=True, parents=True)
        df.to_csv(output_dir / f'parsed_verses.csv', index_label='index', index=True, header=True)
        if not (output_dir / 'vocab.json').is_file():
            with open(output_dir / 'vocab.json', 'w+') as f:
                json.dump(data_constants.SIGN2IDX, f)
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

    print(data_constants.SIGN2IDX)

    df = get_teamim_df(config)
    print(df[df['book'] == 'Gen'].head())
