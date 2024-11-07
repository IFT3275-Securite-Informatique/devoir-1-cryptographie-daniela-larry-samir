from collections import Counter
from typing import List, Dict, Tuple
import nltk
nltk.download('europarl_raw')
from nltk.corpus import europarl_raw
from encrypt import *
import random as rnd
from tqdm import tqdm
from spellchecker import SpellChecker
spell = SpellChecker(language='fr')

def hill_climbing(C, character_freqs, bicharacter_freqs, symbols, iterations=1000):
    all_bytes = [format(i, '08b') for i in range(256)]
    alphabet = symbols[:len(all_bytes)]
    initial_mapping = rnd.sample(alphabet, len(alphabet))
    best_key = dict(zip(all_bytes, initial_mapping))

    # best_key_score = score_text(decrypt(C, best_key), character_freqs, bicharacter_freqs)
    best_key_score = score_text_2(decrypt(C, best_key), character_freqs, bicharacter_freqs)

    for _ in tqdm(range(iterations), desc="Hill Climbing"):
        new_key = change_key(best_key)
        decrypted_text = decrypt(C, new_key)
        # new_key_score = score_text(decrypted_text, character_freqs, bicharacter_freqs)
        new_key_score = score_text_2(decrypted_text, character_freqs, bicharacter_freqs)

        if new_key_score > best_key_score:
            best_key_score = new_key_score
            best_key = new_key

    return best_key_score, best_key

def decrypt(bits, key):
    decrypted_text = []
    for i in range(0, len(bits), 8): 
        byte = bits[i:i+8]
        decrypted_text.append(key.get(byte, '?'))
    return ''.join(decrypted_text)

def score_text(text, letter_freqs, digram_freqs):
    score = 0
    letter_counts = Counter(text)
    for letter, count in letter_counts.items():
        if letter in letter_freqs:
            score += 1 #abs(count * math.log(letter_freqs[letter]))
    
    bicharacters_counts = Counter([text[i:i+2] for i in range(len(text) - 1)])
    for digram, count in bicharacters_counts.items():
        if digram in digram_freqs:
            score += 1 #abs(count * math.log(digram_freqs[digram]))
    return score

def is_french_word(word):
    return word in spell

def score_text_2(text, letter_freqs, digram_freqs):
    score = 0
    splitted_text = text.split(" ")
    #letter_counts = Counter(text)
    for word in splitted_text:
        if is_french_word(word):
            for letter, _ in Counter(word).items():
                if letter in letter_freqs:
                    score += 1

            bicharacters_counts = cut_string_into_pairs(word)
            for digram, _ in Counter(bicharacters_counts).items():
                if digram in digram_freqs:
                    score += 1
    return score

def change_key(key):
    items = list(key.items())
    i, j = rnd.sample(range(len(items)), 2)
    byte_i, byte_j = format(i, '08b'), format(j, '08b')
    key[byte_i], key[byte_j] = key[byte_j], key[byte_i]
    return key

def frequences_analysis_cryptogram(C: str):
  l = len(C)
  ajusted_cryptogram = C

  if l % 8 != 0:
    ajusted_cryptogram = "0" * (8 - (l % 8)) + C

  splitted_cryptogram = [ajusted_cryptogram[i:i + 8] for i in range(0, l, 8)]

  most_common_strings = get_ordered_dict(Counter(splitted_cryptogram))

  return most_common_strings, splitted_cryptogram

def frequences_analysis_plain_text(text: str) -> Tuple[Dict, Dict]:
  most_common_caracters = get_ordered_dict(Counter(text))
  most_common_bicaracters = get_ordered_dict(Counter(cut_string_into_pairs(text)))
  return most_common_caracters, most_common_bicaracters

def get_ordered_dict(frequences: Counter) -> Dict:
  tuples = frequences.most_common()
  tot = sum(t[1] for t in tuples)
  result = {}
  for s, v in tuples:
    result[s] = v / tot
  return result

if __name__ == '__main__':
    french_text = europarl_raw.french.raw()
    most_common_caracters, most_common_bicaracters = frequences_analysis_plain_text(french_text)
    C = ("0100000000001000000011100011000110001110010111101111010111011010010101100110000100001010010000000111001001011110111101011101101000001000" +
         "00001110001100011010001110101111011000110111101100110001110001010000001100100110000011100011000100100000110011100110000101110001000010100" +
         "100000010110110000000111100111001100001001100011100010101000110000011100011000110100011101011110110001101111011110001100101001101011101001" +
         "01101011100001001010001010101")
    
    symbols = ['Q', ';', 'h', '\ufeff', 'e', 's', '6', ' ', 'ê', 'ç', 'V', 'â', 'À', 'J', '“', 'A', 'È', 'R', 'G', '—', '*', 'T', 'à', 'Z', 'm',
               '\r', '™', '2', 'Î', 'Â', 'Ê', '‘', ')', '7', 'l', 'q', 'f', 'o', '1', 'ô', 'U', 'û', 'H', 'S', 'N', 'î', 'C', 'u', 'O', '!', 'ï',
                'º', '4', ',', 'P', '5', '[', 'X', 'v', '$', 'è', ':', '.', '#', '3', 'W', '°', 'y', '»', '…', '0', 'g', '”', 'L', '8', '•', 'Y',
                'j', 'k', 'r', '/', '9', 'c', 'K', 'D', '-', 'ù', 'n', 'E', 'b', '_', 'é', 'M', '«', 'I', 'Ç', '\n', 'a', '’', 'w', 'z', "'", 'x',
                ']', 'F', '?', '(', '%', 'É', 'p', 'B', 't', 'ë', 'i', 'd', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de',
                'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er',
                ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa',
                'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro',
                'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu',
                "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét',
                'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
    best_key_score, best_key = hill_climbing(C, most_common_caracters, most_common_bicaracters, symbols, 10000000)
    R = decrypt(C, best_key)
    print(R)
